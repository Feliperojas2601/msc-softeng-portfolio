from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from adapters.database.credit_card_model import CreditCardModel
from adapters.database.verification_outbox import VerificationOutboxModel
from domain.models.credit_card import CreditCard, CreditCardIssuer, CreditCardStatus
from domain.ports.credit_card_repository_port import CreditCardRepositoryPort


class SQLAlchemyCreditCardRepository(CreditCardRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def create(self, credit_card: CreditCard) -> CreditCard:
        model = CreditCardModel(
            id=credit_card.id,
            token=credit_card.token,
            user_id=credit_card.user_id,
            last_four_digits=credit_card.last_four_digits,
            ruv=credit_card.ruv,
            issuer=credit_card.issuer.value,
            status=credit_card.status.value,
            created_at=credit_card.created_at,
            updated_at=credit_card.updated_at,
        )
        self.session.add(model)
        if credit_card.status == CreditCardStatus.POR_VERIFICAR and credit_card.ruv:
            self.session.flush()
            self.session.add(
                VerificationOutboxModel(
                    card_id=credit_card.id,
                    event_id=str(uuid4()),
                    ruv=credit_card.ruv,
                    available_at=datetime.now(UTC),
                )
            )
        self.session.commit()
        self.session.refresh(model)
        return credit_card

    def exists_for_user(self, user_id: str, token: str) -> bool:
        return (
            self.session.scalar(
                select(CreditCardModel.id)
                .where(
                    CreditCardModel.user_id == user_id,
                    CreditCardModel.token == token,
                )
                .limit(1)
            )
            is not None
        )

    def get_by_id(self, card_id: str) -> CreditCard | None:
        model = self.session.get(CreditCardModel, card_id)
        if model is None:
            return None
        return CreditCard(
            id=model.id,
            token=model.token,
            user_id=model.user_id,
            last_four_digits=model.last_four_digits,
            ruv=model.ruv,
            issuer=CreditCardIssuer(model.issuer),
            status=CreditCardStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def list_by_user(self, user_id: str) -> list[CreditCard]:
        models = self.session.scalars(
            select(CreditCardModel)
            .where(CreditCardModel.user_id == user_id)
            .order_by(CreditCardModel.created_at, CreditCardModel.id)
        )
        return [
            CreditCard(
                id=model.id,
                token=model.token,
                user_id=model.user_id,
                last_four_digits=model.last_four_digits,
                ruv=model.ruv,
                issuer=CreditCardIssuer(model.issuer),
                status=CreditCardStatus(model.status),
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
            for model in models
        ]

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(CreditCardModel))

    def reset(self) -> None:
        self.session.execute(delete(VerificationOutboxModel))
        self.session.execute(delete(CreditCardModel))
        self.session.commit()

    def finalize_verification(self, card_id: str, status: str) -> CreditCard | None:
        model = self.session.scalar(
            select(CreditCardModel)
            .where(CreditCardModel.id == card_id)
            .with_for_update()
        )
        if model is None:
            return None
        current_status = CreditCardStatus(model.status)
        requested_status = CreditCardStatus(status)
        if current_status == CreditCardStatus.POR_VERIFICAR:
            model.status = requested_status.value
            model.updated_at = datetime.now(UTC)
            self.session.commit()
            self.session.refresh(model)
        elif current_status != requested_status:
            self.session.rollback()
            from errors import InvalidVerificationTransitionError

            raise InvalidVerificationTransitionError()
        return CreditCard(
            id=model.id,
            token=model.token,
            user_id=model.user_id,
            last_four_digits=model.last_four_digits,
            ruv=model.ruv,
            issuer=CreditCardIssuer(model.issuer),
            status=CreditCardStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
