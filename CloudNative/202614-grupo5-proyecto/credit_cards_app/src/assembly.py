from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from adapters.http.payment_provider_adapter import HttpPaymentProviderAdapter
from adapters.http.users_adapter import HttpUsersAdapter
from config import settings
from entrypoints.api.routers.credit_card_router import router
from errors import (
    DuplicateCardError,
    ExpiredCardError,
    InvalidCardDataError,
    InvalidTokenError,
    PaymentProviderRejectedError,
    PaymentProviderUnavailableError,
    UsersUnavailableError,
)


def create_app(session_factory=None, users=None) -> Flask:
    app = Flask(__name__)
    if session_factory is None:
        from adapters.database.session import session_factory

    app.extensions["credit_cards_session_factory"] = session_factory
    app.extensions["credit_cards_users"] = (
        users
        if users is not None
        else HttpUsersAdapter(settings.users_app_url, settings.users_timeout_seconds)
    )
    app.extensions["credit_cards_payment_provider"] = HttpPaymentProviderAdapter(
        settings.true_native_base_url,
        settings.true_native_secret_token,
        settings.true_native_timeout_seconds,
    )
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = settings.credit_cards_internal_secret
    app.register_blueprint(router)

    @app.errorhandler(InvalidTokenError)
    def invalid_token(error):
        return "", 401

    @app.errorhandler(UsersUnavailableError)
    @app.errorhandler(SQLAlchemyError)
    def unavailable(error):
        return "", 503

    @app.errorhandler(InvalidCardDataError)
    def invalid_card_data(error):
        return "", 400

    @app.errorhandler(DuplicateCardError)
    def duplicate_card(error):
        return "", 409

    @app.errorhandler(ExpiredCardError)
    def expired_card(error):
        return "", 412

    @app.errorhandler(PaymentProviderRejectedError)
    @app.errorhandler(PaymentProviderUnavailableError)
    def rejected_card(error):
        return "", 503 if isinstance(error, PaymentProviderUnavailableError) else 400

    return app
