import json
import logging
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

logger = logging.getLogger(__name__)


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class PollingError(Exception):
    pass


class InvalidMessageError(PollingError):
    pass


class ProviderResponseError(PollingError):
    pass


class InternalApiError(PollingError):
    pass


class NotificationError(PollingError):
    pass


@dataclass(frozen=True)
class Settings:
    true_native_base_url: str
    true_native_secret_token: str
    cards_api_base_url: str
    cards_api_secret: str
    users_api_base_url: str = ""
    notifications_api_base_url: str = ""
    request_timeout_seconds: float = 5.0

    @classmethod
    def from_env(cls) -> "Settings":
        values = {
            "true_native_base_url": os.environ.get("TRUE_NATIVE_BASE_URL", ""),
            "true_native_secret_token": os.environ.get("TRUE_NATIVE_SECRET_TOKEN", ""),
            "cards_api_base_url": os.environ.get("CARDS_API_BASE_URL", ""),
            "cards_api_secret": os.environ.get("CARDS_API_SECRET", ""),
            "users_api_base_url": os.environ.get("USERS_API_BASE_URL", ""),
            "notifications_api_base_url": os.environ.get(
                "NOTIFICATIONS_API_BASE_URL", ""
            ),
        }
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise PollingError(f"missing configuration: {', '.join(missing)}")
        return cls(**values)


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: Any


HttpRequest = Any  # Callable[[str, str, str, Any | None, float], HttpResponse]


def _decode_body(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw.decode("utf-8", errors="replace")


def http_request(
    method: str,
    url: str,
    token: str,
    payload: Any | None,
    timeout: float,
) -> HttpResponse:
    encoded = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=encoded,
        method=method,
        headers={
            "Accept": "application/json",
            **({"Authorization": f"Bearer {token}"} if token else {}),
            **({"Content-Type": "application/json"} if encoded else {}),
        },
    )
    try:
        with build_opener(NoRedirects()).open(request, timeout=timeout) as response:
            return HttpResponse(response.status, _decode_body(response.read()))
    except HTTPError as error:
        return HttpResponse(error.code, _decode_body(error.read()))
    except (URLError, TimeoutError, OSError) as error:
        raise ProviderResponseError("upstream request failed") from error


def _event_payload(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise InvalidMessageError("event must be an object")
    for field in ("cardId", "ruv", "eventId", "leaseId"):
        if not isinstance(event.get(field), str) or not event[field].strip():
            raise InvalidMessageError(f"event field {field} is required")
    return {field: event[field] for field in ("cardId", "ruv", "eventId", "leaseId")}


def _normalized(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return "".join(value.upper().split()).replace("-", "_")


def _terminal_status(body: Any) -> str | None:
    if isinstance(body, dict):
        for key in (
            "status",
            "cardStatus",
            "state",
            "result",
            "task_status",
            "taskStatus",
        ):
            status = _terminal_status(body.get(key))
            if status:
                return status
        if isinstance(body.get("approved"), bool):
            return "APROBADA" if body["approved"] else "RECHAZADA"
        for value in body.values():
            status = _terminal_status(value)
            if status:
                return status
    elif isinstance(body, str):
        value = _normalized(body)
        if value in {
            "APPROVED",
            "APROBADA",
            "VERIFIED",
            "VERIFICADA",
        }:
            return "APROBADA"
        if value in {"REJECTED", "RECHAZADA", "DECLINED", "DENIED"}:
            return "RECHAZADA"
    return None


def _card_data(response: HttpResponse, payload: dict[str, Any]) -> dict[str, Any]:
    if response.status_code != 200 or not isinstance(response.body, dict):
        raise InternalApiError("credit cards API did not return verification data")
    card = response.body
    if card.get("id") != payload["cardId"] or card.get("ruv") != payload["ruv"]:
        raise InternalApiError("card identity does not match verification message")
    if not isinstance(card.get("userId"), str) or not card["userId"].strip():
        raise InternalApiError("card owner is missing")
    if card.get("status") not in ("POR_VERIFICAR", "APROBADA", "RECHAZADA"):
        raise InternalApiError("invalid stored card status")
    return card


def _notify(card: dict[str, Any], settings: Settings, request_fn: HttpRequest) -> None:
    if not settings.users_api_base_url or not settings.notifications_api_base_url:
        raise NotificationError("notification service configuration is missing")
    user_response = request_fn(
        "GET",
        f"{settings.users_api_base_url.rstrip('/')}/users/{quote(card['userId'], safe='')}",
        "",
        None,
        settings.request_timeout_seconds,
    )
    user = user_response.body
    if (
        user_response.status_code != 200
        or not isinstance(user, dict)
        or user.get("id") != card["userId"]
        or not isinstance(user.get("email"), str)
        or not user["email"].strip()
        or (user.get("fullName") is not None and not isinstance(user["fullName"], str))
    ):
        raise NotificationError("user contact data is unavailable")
    notification = {
        "type": "CREDIT_CARD_VERIFICATION",
        "userId": card["userId"],
        "email": user["email"],
        "fullName": user.get("fullName"),
        "status": "VERIFICADA" if card["status"] == "APROBADA" else "RECHAZADA",
        "ruv": card["ruv"],
    }
    for field in ("lastFourDigits", "franchise"):
        if card.get(field) is not None:
            if not isinstance(card[field], str):
                raise NotificationError("invalid card notification data")
            notification[field] = card[field]
    response = request_fn(
        "POST",
        f"{settings.notifications_api_base_url.rstrip('/')}/notify",
        "",
        notification,
        settings.request_timeout_seconds,
    )
    if response.status_code != 200:
        raise NotificationError(
            f"notifications API returned HTTP {response.status_code}"
        )


def _ack(payload: dict[str, Any], settings: Settings, request_fn: HttpRequest) -> None:
    ack_url = (
        f"{settings.cards_api_base_url.rstrip('/')}/credit-cards/internal/"
        f"verification-events/{quote(payload['eventId'], safe='')}/ack"
    )
    response = request_fn(
        "POST",
        ack_url,
        settings.cards_api_secret,
        {"leaseId": payload["leaseId"]},
        settings.request_timeout_seconds,
    )
    if response.status_code < 200 or response.status_code >= 300:
        raise InternalApiError(
            f"failed to acknowledge verification event: HTTP {response.status_code}"
        )


def process_event(
    event: dict[str, Any],
    settings: Settings,
    request_fn: HttpRequest = http_request,
) -> str:
    payload = _event_payload(event)
    update_url = (
        f"{settings.cards_api_base_url.rstrip('/')}/credit-cards/internal/"
        f"{quote(payload['cardId'], safe='')}/verification"
    )
    card = _card_data(
        request_fn(
            "GET",
            update_url,
            settings.cards_api_secret,
            None,
            settings.request_timeout_seconds,
        ),
        payload,
    )
    if card["status"] in ("APROBADA", "RECHAZADA"):
        _notify(card, settings, request_fn)
        _ack(payload, settings, request_fn)
        return card["status"]
    native_url = (
        f"{settings.true_native_base_url.rstrip('/')}/native/cards/"
        f"{quote(payload['ruv'], safe='')}"
    )
    response = request_fn(
        "GET",
        native_url,
        settings.true_native_secret_token,
        None,
        settings.request_timeout_seconds,
    )
    if response.status_code == 202:
        release_url = (
            f"{settings.cards_api_base_url.rstrip('/')}/credit-cards/internal/"
            f"verification-events/{quote(payload['eventId'], safe='')}/release"
        )
        released = request_fn(
            "POST",
            release_url,
            settings.cards_api_secret,
            {"leaseId": payload["leaseId"]},
            settings.request_timeout_seconds,
        )
        if released.status_code != 200:
            raise InternalApiError(
                f"failed to release verification event: HTTP {released.status_code}"
            )
        return "PENDING"
    if response.status_code < 200 or response.status_code >= 300:
        raise ProviderResponseError(f"TrueNative returned HTTP {response.status_code}")
    status = _terminal_status(response.body)
    if status is None:
        raise ProviderResponseError("TrueNative response has no terminal status")
    update = request_fn(
        "PATCH",
        update_url,
        settings.cards_api_secret,
        {"status": status, "eventId": payload["eventId"]},
        settings.request_timeout_seconds,
    )
    if update.status_code < 200 or update.status_code >= 300:
        raise InternalApiError(f"credit cards API returned HTTP {update.status_code}")
    card = _card_data(update, payload)
    if card["status"] != status:
        raise InternalApiError("persisted result does not match provider result")
    _notify(card, settings, request_fn)
    _ack(payload, settings, request_fn)
    return status


def claim_events(
    settings: Settings, request_fn: HttpRequest = http_request
) -> list[dict[str, Any]]:
    claim_url = (
        f"{settings.cards_api_base_url.rstrip('/')}/credit-cards/internal/"
        "verification-events/claim"
    )
    response = request_fn(
        "POST",
        claim_url,
        settings.cards_api_secret,
        {},
        settings.request_timeout_seconds,
    )
    if response.status_code != 200 or not isinstance(response.body, list):
        raise InternalApiError(
            f"failed to claim verification events: HTTP {response.status_code}"
        )
    return response.body


def run_once(settings: Settings) -> tuple[int, int]:
    events = claim_events(settings)
    processed = 0
    failed = 0
    for claimed in events:
        try:
            process_event(claimed, settings)
            processed += 1
        except Exception as error:  # noqa: BLE001
            logger.warning("Card verification event failed: %s", type(error).__name__)
            failed += 1
    return processed, failed
