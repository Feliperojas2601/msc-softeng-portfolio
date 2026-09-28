from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from adapters.database.credit_card_model import CreditCardModel
from config import settings

engine = create_engine(settings.database_url, future=True)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


def init_models() -> None:
    CreditCardModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    with session_factory() as session:
        yield session
