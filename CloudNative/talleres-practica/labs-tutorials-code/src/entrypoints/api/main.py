import logging
import re

from aws_lambda_powertools.event_handler import (
    APIGatewayHttpResolver,
    Response,
    content_types,
)

from assembly import build_calculate_use_case
from domain.models.operation import Operation
from errors import DivisionByZeroError, InvalidOperationError, ValidationError

app = APIGatewayHttpResolver(strip_prefixes=[re.compile(r"/v[1-3]+")])


def _extract_model_from_event(event: dict) -> Operation:
    """Creates operation from the event."""
    json_body = event.json_body
    return Operation(
        number1=json_body.get("number1"),
        number2=json_body.get("number2"),
        sign=json_body.get("sign"),
    )


@app.exception_handler(DivisionByZeroError)
@app.exception_handler(InvalidOperationError)
@app.exception_handler(ValidationError)
def handler_custom_error(exc: Exception) -> Response:
    """Catch all the custom errors."""
    logging.error(str(exc), stack_info=True, exc_info=True)
    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        body={"error": str(exc)},
    )


@app.exception_handler(Exception)
def handler_unexpected_error(exc: Exception) -> Response:
    """Catch all the unexpected exceptions."""
    logging.error(str(exc), stack_info=True, exc_info=True)
    return Response(
        status_code=503,
        content_type=content_types.APPLICATION_JSON,
        body={"error": str(exc)},
    )


@app.get("/ping")
def health() -> Response:
    """Healthcheck."""
    return Response(
        status_code=200,
        content_type=content_types.TEXT_PLAIN,
        body="pong",
    )


@app.post("/calculate")
def execute_calculation(use_case=build_calculate_use_case()) -> Response:
    """Creates the operation and calls the use case."""
    operation = _extract_model_from_event(app.current_event)
    result = use_case.execute(operation)
    return Response(
        status_code=200,
        content_type=content_types.APPLICATION_JSON,
        body={"data": {"result": result}},
    )


def handler(event, context) -> dict:
    """Entrypoint function."""
    logging.debug(event)
    return app.resolve(event, context)
