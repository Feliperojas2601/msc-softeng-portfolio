from adapters.http.client import request
from domain.ports.identity_verification_port import IdentityVerificationPort
from errors import IdentityVerificationRequestError


class TrueNativeIdentityVerificationAdapter(IdentityVerificationPort):
    """TrueNative implementation of IdentityVerificationPort (POST /native/verify)."""

    def __init__(
        self,
        base_url: str,
        secret_token: str,
        timeout: float = 5.0,
        max_retries: int = 0,
    ):
        self._base_url = base_url.rstrip("/")
        self._secret_token = secret_token
        self._timeout = timeout
        self._max_retries = max_retries

    async def request_verification(
        self,
        user_id: str,
        transaction_identifier: str,
        webhook_url: str,
        email: str,
        dni: str | None = None,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> None:
        """Call TrueNative's verify endpoint; raises if it cannot be reached or rejects it."""
        payload = {
            "user": {
                "email": email,
                "dni": dni,
                "fullName": full_name,
                "phone": phone_number,
            },
            "transactionIdentifier": transaction_identifier,
            "userIdentifier": user_id,
            "userWebhook": webhook_url,
        }

        response = await request(
            "POST",
            f"{self._base_url}/native/verify",
            timeout=self._timeout,
            max_retries=self._max_retries,
            json=payload,
            headers={"Authorization": f"Bearer {self._secret_token}"},
        )

        if response.status_code != 201:
            raise IdentityVerificationRequestError(
                f"TrueNative returned {response.status_code}"
            )
