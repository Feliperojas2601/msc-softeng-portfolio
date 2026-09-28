# syntax=docker/dockerfile:1

FROM python:3.13.7-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

COPY --chown=app:app src ./src

USER app

CMD ["python", "src/worker.py"]
