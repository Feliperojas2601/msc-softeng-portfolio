# Notifications App

Componente que recibe el resultado de los procesos de verificación (identidad, RF-007, y tarjetas de crédito, RF-006) y lo publica en un Topic de **AWS SNS**, cuya suscripción de correo entrega el resultado a la dirección configurada en `EMAIL_TO_NOTIFY`. Construido en Python con FastAPI, siguiendo la misma arquitectura hexagonal liviana que `identity_webhook_app`.

No tiene base de datos propia ni ruta pública en el Ingress: es un componente puramente interno, alcanzado solo por otros pods del clúster (`identity_webhook_app` y `credit_cards_app` lo llaman a él; no llama a ningún otro servicio de dominio).

## Tabla de contenido

- [Notifications App](#notifications-app)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Por qué existe este componente](#por-qué-existe-este-componente)
  - [Por qué SNS en vez de HTTP/SES/SMTP propio](#por-qué-sns-en-vez-de-httpsessmtp-propio)
  - [Requisitos](#requisitos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Flujo](#flujo)
  - [Contrato de entrada](#contrato-de-entrada)
  - [Configuración](#configuración)
  - [Ejecución local](#ejecución-local)
  - [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
  - [Pruebas](#pruebas)

## Por qué existe este componente

RF-006 y RF-007 exigen notificar por correo el resultado de cada verificación (identidad o tarjeta), independientemente de si fue exitosa o rechazada. En vez de que cada productor del evento (`identity_webhook_app`, `credit_cards_app`) implemente su propio envío de correo y maneje credenciales de AWS, ese trabajo se concentra en un único componente: `notifications_app` es el **único** lugar del sistema que conoce el mecanismo de entrega y el **único** que necesita permiso `sns:Publish`. Los productores solo saben que existe un `POST /notify`.

Esto además respeta la restricción de propiedad de datos: `notifications_app` nunca lee `users DB` ni `credit-card DB` — toda la información que necesita para armar el correo (correo, nombre, estado, RUV, datos básicos de la tarjeta) viaja en el cuerpo de la petición.

## Por qué SNS en vez de HTTP/SES/SMTP propio

Se evaluó descartar SNS por la misma razón que llevó a `identity_webhook_app` a descartar Lambda (la cuenta de AWS Academy Learner Lab no permite crear roles ni políticas IAM nuevos, solo reutilizar roles existentes). Se validó explícitamente que **sí es viable para un contenedor** (a diferencia de un Lambda, que necesita su propio rol de ejecución):

- Un Topic de SNS con una suscripción de tipo `email` entrega el correo directamente — no hace falta SES, SMTP ni código de envío propio.
- El contenedor solo necesita el permiso `sns:Publish`, usando las credenciales de sesión temporales que ya usa el pipeline para Terraform (inyectadas como variable de entorno al Pod). No se crea ningún rol IAM nuevo.
- Se probó de punta a punta (`CreateTopic`, `Publish`, `Subscribe` con protocolo `email`) contra una cuenta real de AWS Academy antes de construir este componente.

## Requisitos

- Python 3.11
- Poetry 2.1.1
- Docker / Docker Compose
- Credenciales de AWS con permiso `sns:Publish` sobre el Topic configurado (para ejecución local real; los tests no requieren credenciales válidas)

## Estructura del proyecto

```
.
├── src/
│   ├── config.py                     # Settings desde variables de ambiente
│   ├── errors.py
│   ├── assembly.py                   # Wiring de dependencias
│   ├── domain/
│   │   ├── ports/                    # NotificationPublisherPort
│   │   └── use_cases/                # SendNotificationUseCase (arma el correo por tipo)
│   ├── adapters/
│   │   └── sns/                      # SnsNotificationPublisherAdapter (boto3)
│   └── entrypoints/
│       └── api/
│           ├── main.py               # FastAPI app + manejo de excepciones
│           ├── routers/              # POST /notify, GET /ping
│           └── schemas/              # DTO del contrato de entrada
├── tests/unit/                       # Misma estructura que src/, sin red/AWS real
├── Dockerfile
└── pyproject.toml
```

## Flujo

1. `identity_webhook_app` o `credit_cards_app` hacen `POST /notify` con el resultado del proceso.
2. Se valida el cuerpo contra el contrato (campo `type` determina si es `IDENTITY_VERIFICATION` o `CREDIT_CARD_VERIFICATION`).
3. `SendNotificationUseCase` arma el asunto y el cuerpo del correo según el tipo (incluye estado, RUV, y — para tarjetas — los últimos 4 dígitos y la franquicia).
4. Se publica el mensaje al Topic de SNS (`sns:Publish`). SNS entrega el correo a la suscripción de `EMAIL_TO_NOTIFY`.
5. Se responde `200` al productor. Si la publicación falla, se responde `502` — el productor ya trata esta llamada como best-effort (loguea y continúa, no revierte el cambio de estado que ya aplicó en su propio dominio).

## Contrato de entrada

`POST /notify`:

```json
{
  "type": "IDENTITY_VERIFICATION",
  "userId": "string",
  "email": "string",
  "fullName": "string | null",
  "status": "VERIFICADO | NO_VERIFICADO",
  "ruv": "string"
}
```

o, para tarjetas:

```json
{
  "type": "CREDIT_CARD_VERIFICATION",
  "userId": "string",
  "email": "string",
  "fullName": "string | null",
  "status": "VERIFICADA | RECHAZADA",
  "ruv": "string",
  "lastFourDigits": "string",
  "franchise": "string"
}
```

`lastFourDigits` y `franchise` son opcionales en el esquema (ignorados si el tipo es `IDENTITY_VERIFICATION`).

## Configuración

Variables de ambiente:

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto en el que escucha. | `30008` |
| `AWS_REGION` | Región de AWS del Topic de SNS. | `us-east-1` |
| `SNS_TOPIC_ARN` | ARN del Topic al que se publica. | — (obligatorio en despliegue real) |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` | Credenciales leídas directamente por `boto3` (no son variables propias de la app). En AWS se inyectan como Secret de Kubernetes con las mismas credenciales de sesión que usa el pipeline. | — |

## Ejecución local

Requiere credenciales de AWS válidas exportadas en la terminal (boto3 las lee del entorno del proceso, no del archivo `.env`):

```bash
cd notifications_app
cp .env.example .env
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=...
poetry install
poetry run uvicorn entrypoints.api.main:app --app-dir src --reload --port 30008
```

## Ejecutar con Docker Compose

```bash
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=...
docker compose up --build
```

## Pruebas

```bash
poetry run pytest tests/unit --cov=src --cov-report=term-missing
poetry run ruff check src tests
poetry run black --check src tests
```

No requieren credenciales de AWS reales ni red: el cliente de SNS se mockea (`unittest.mock`), y `pytest.ini` (en `pyproject.toml`) fija credenciales ficticias para que `boto3.client(...)` se pueda construir sin errores incluso si algún test lo instancia sin mockear explícitamente.

Las pruebas unitarias de este componente son opcionales para la calificación de la entrega (según las restricciones), pero se mantienen como estándar del equipo.
