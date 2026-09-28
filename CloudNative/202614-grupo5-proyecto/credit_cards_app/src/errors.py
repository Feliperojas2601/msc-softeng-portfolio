class CreditCardsError(Exception):
    pass


class InvalidTokenError(CreditCardsError):
    pass


class UsersUnavailableError(CreditCardsError):
    pass


class InvalidCardDataError(CreditCardsError):
    pass


class DuplicateCardError(CreditCardsError):
    pass


class ExpiredCardError(CreditCardsError):
    pass


class PaymentProviderUnavailableError(CreditCardsError):
    pass


class PaymentProviderRejectedError(CreditCardsError):
    pass


class CreditCardNotFoundError(CreditCardsError):
    pass


class InvalidVerificationTransitionError(CreditCardsError):
    pass
