from uuid import uuid4

import httpx

from domain.ports.payment_provider_port import (
    PaymentProviderPort,
    PaymentTokenizationResult,
)
from errors import (
    DuplicateCardError,
    ExpiredCardError,
    PaymentProviderRejectedError,
    PaymentProviderUnavailableError,
)


class HttpPaymentProviderAdapter(PaymentProviderPort):
    def __init__(self, base_url: str, secret_token: str, timeout: float):
        self.url = f"{base_url.rstrip('/')}/native/cards"
        self.secret_token = secret_token
        self.timeout = timeout

    def tokenize(
        self,
        *,
        card_number: str,
        cvv: str,
        expiration_date: str,
        card_holder_name: str,
    ) -> PaymentTokenizationResult:
        try:
            response = httpx.post(
                self.url,
                headers={"Authorization": f"Bearer {self.secret_token}"},
                json={
                    "transactionIdentifier": str(uuid4()),
                    "card": {
                        "cardNumber": card_number,
                        "cvv": cvv,
                        "expirationDate": expiration_date,
                        "cardHolderName": card_holder_name,
                    },
                },
                timeout=self.timeout,
                follow_redirects=False,
            )
        except httpx.RequestError as exc:
            raise PaymentProviderUnavailableError() from exc
        if response.status_code == 409:
            raise DuplicateCardError()
        if response.status_code == 412:
            raise ExpiredCardError()
        if response.status_code not in (200, 201):
            if 400 <= response.status_code < 500:
                raise PaymentProviderRejectedError()
            raise PaymentProviderUnavailableError()
        try:
            payload = response.json()
        except ValueError as exc:
            raise PaymentProviderUnavailableError() from exc
        if not isinstance(payload, dict):
            raise PaymentProviderUnavailableError()
        values = (
            payload.get("data") if isinstance(payload.get("data"), dict) else payload
        )
        token = (
            values.get("token") or values.get("cardToken") or values.get("card_token")
        )
        if not isinstance(token, str) or not token or len(token) > 256:
            raise PaymentProviderUnavailableError()
        issuer = (
            values.get("issuer")
            or values.get("franchise")
            or values.get("cardBrand")
            or "UNKNOWN"
        )
        if not isinstance(issuer, str):
            issuer = "UNKNOWN"
        ruv = values.get("ruv") or values.get("RUV")
        if ruv is not None:
            if not isinstance(ruv, str) or not ruv.strip() or len(ruv) > 256:
                raise PaymentProviderUnavailableError()
            ruv = ruv.strip()
        return PaymentTokenizationResult(token=token, issuer=issuer, ruv=ruv)
