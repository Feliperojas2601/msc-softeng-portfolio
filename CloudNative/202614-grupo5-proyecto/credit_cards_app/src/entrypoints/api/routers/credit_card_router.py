from hmac import compare_digest

from flask import Blueprint, Response, current_app, jsonify, request

from adapters.database.credit_card_repository import SQLAlchemyCreditCardRepository
from adapters.database.verification_outbox import VerificationOutboxRepository
from domain.use_cases.count_credit_cards_use_case import CountCreditCardsUseCase
from domain.use_cases.create_credit_card_use_case import CreateCreditCardUseCase
from domain.use_cases.finalize_credit_card_verification_use_case import (
    FinalizeCreditCardVerificationUseCase,
)
from domain.use_cases.list_credit_cards_use_case import ListCreditCardsUseCase
from domain.use_cases.reset_credit_cards_use_case import ResetCreditCardsUseCase
from entrypoints.api.schemas.credit_card_schemas import serialize_credit_card
from errors import (
    CreditCardNotFoundError,
    InvalidCardDataError,
    InvalidVerificationTransitionError,
)

router = Blueprint("credit_cards", __name__, url_prefix="/credit-cards")


def _bearer_token() -> tuple[str | None, int | None]:
    authorization = request.headers.get("Authorization", "").strip()
    if not authorization:
        return None, 403
    parts = authorization.split()
    if len(parts) == 1 and parts[0].lower() == "bearer":
        return None, 403
    if (
        len(parts) != 2
        or parts[0].lower() != "bearer"
        or not parts[1].isascii()
        or not parts[1].isprintable()
    ):
        return None, 401
    return parts[1], None


def _internal_service_authorized() -> tuple[bool, int]:
    authorization = request.headers.get("Authorization", "").strip()
    expected = current_app.config.get("CREDIT_CARDS_INTERNAL_SECRET", "")
    if not expected:
        return False, 503
    parts = authorization.split()
    if not authorization or len(parts) != 2 or parts[0].lower() != "bearer":
        return False, 403 if not authorization else 401
    authorized = compare_digest(parts[1].encode(), expected.encode())
    return authorized, 200 if authorized else 401


@router.get("/ping")
def ping() -> Response:
    return current_app.response_class("pong", mimetype="text/plain")


@router.get("")
def list_credit_cards():
    token, error = _bearer_token()
    if error is not None:
        return "", error
    with current_app.extensions["credit_cards_session_factory"]() as session:
        use_case = ListCreditCardsUseCase(
            SQLAlchemyCreditCardRepository(session),
            current_app.extensions["credit_cards_users"],
        )
        cards = use_case.execute(token)
        return jsonify([serialize_credit_card(card) for card in cards])


@router.post("")
def create_credit_card():
    token, error = _bearer_token()
    if error is not None:
        return "", error
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise InvalidCardDataError()
    fields = ("cardNumber", "cvv", "expirationDate", "cardHolderName")
    if any(field not in body for field in fields):
        raise InvalidCardDataError()
    with current_app.extensions["credit_cards_session_factory"]() as session:
        user_id = current_app.extensions["credit_cards_users"].get_user_id(token)
        card = CreateCreditCardUseCase(
            SQLAlchemyCreditCardRepository(session),
            current_app.extensions["credit_cards_payment_provider"],
        ).execute(
            user_id=user_id,
            card_number=body["cardNumber"],
            cvv=str(body["cvv"]) if isinstance(body["cvv"], int) else body["cvv"],
            expiration_date=body["expirationDate"],
            card_holder_name=body["cardHolderName"],
        )
    return jsonify(
        id=card.id,
        userId=card.user_id,
        createdAt=card.created_at.isoformat(timespec="seconds"),
    ), 201


@router.post("/internal/verification-events/claim")
def claim_verification_events():
    authorized, error = _internal_service_authorized()
    if not authorized:
        return "", error
    with current_app.extensions["credit_cards_session_factory"]() as session:
        events = VerificationOutboxRepository(session).claim()
    return jsonify(events)


@router.post("/internal/verification-events/<event_id>/ack")
def acknowledge_verification_event(event_id):
    authorized, error = _internal_service_authorized()
    if not authorized:
        return "", error
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not isinstance(body.get("leaseId"), str):
        return "", 400
    with current_app.extensions["credit_cards_session_factory"]() as session:
        acknowledged = VerificationOutboxRepository(session).acknowledge(
            event_id, body["leaseId"]
        )
    if not acknowledged:
        return "", 409
    return jsonify(published=True)


@router.post("/internal/verification-events/<event_id>/release")
def release_verification_event(event_id):
    authorized, error = _internal_service_authorized()
    if not authorized:
        return "", error
    body = request.get_json(silent=True)
    if (
        not isinstance(body, dict)
        or not isinstance(body.get("leaseId"), str)
        or not body["leaseId"].strip()
    ):
        return "", 400
    with current_app.extensions["credit_cards_session_factory"]() as session:
        released = VerificationOutboxRepository(session).release(
            event_id, body["leaseId"]
        )
    if not released:
        return "", 409
    return jsonify(scheduled=True)


@router.get("/count")
def count_credit_cards():
    with current_app.extensions["credit_cards_session_factory"]() as session:
        count = CountCreditCardsUseCase(
            SQLAlchemyCreditCardRepository(session)
        ).execute()
        return jsonify(count=count)


@router.post("/reset")
def reset_credit_cards():
    with current_app.extensions["credit_cards_session_factory"]() as session:
        ResetCreditCardsUseCase(SQLAlchemyCreditCardRepository(session)).execute()
    return jsonify(msg="Todos los datos fueron eliminados")


def _verification_data(card):
    return {
        "id": card.id,
        "userId": card.user_id,
        "ruv": card.ruv,
        "lastFourDigits": card.last_four_digits,
        "franchise": card.issuer.value,
        "status": card.status.value,
        "updatedAt": card.updated_at.isoformat(timespec="seconds"),
    }


@router.get("/internal/<card_id>/verification")
def get_credit_card_verification(card_id: str):
    authorized, error = _internal_service_authorized()
    if not authorized:
        return "", error
    with current_app.extensions["credit_cards_session_factory"]() as session:
        card = SQLAlchemyCreditCardRepository(session).get_by_id(card_id)
        if card is None:
            return "", 404
        return jsonify(_verification_data(card))


@router.patch("/internal/<card_id>/verification")
def finalize_credit_card_verification(card_id: str):
    authorized, error = _internal_service_authorized()
    if not authorized:
        return "", error
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not isinstance(body.get("status"), str):
        return "", 400
    with current_app.extensions["credit_cards_session_factory"]() as session:
        try:
            card = FinalizeCreditCardVerificationUseCase(
                SQLAlchemyCreditCardRepository(session)
            ).execute(card_id, body["status"])
        except CreditCardNotFoundError:
            return "", 404
        except (InvalidVerificationTransitionError, ValueError):
            return "", 409
    return jsonify(_verification_data(card))
