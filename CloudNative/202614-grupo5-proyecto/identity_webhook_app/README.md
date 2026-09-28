# Identity Webhook App

Componente que recibe el callback (webhook) de **TrueNative** con el resultado de la verificación de identidad de un usuario (RF-007), actualiza el estado final del usuario en `users_app` y notifica el resultado al componente de notificaciones. Construido en Python con FastAPI, siguiendo la misma arquitectura hexagonal liviana que `orchestrator_app`.

No tiene base de datos propia ni ruta pública en el Ingress: es un componente puramente interno, alcanzado solo por otros pods del cluster (TrueNative llamándolo, y users_app/otros no lo llaman a él).

## Tabla de contenido

- [Identity Webhook App](#identity-webhook-app)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Por qué existe este componente](#por-qué-existe-este-componente)
  - [Por qué es un contenedor y no un Lambda](#por-qué-es-un-contenedor-y-no-un-lambda)
  - [Requisitos](#requisitos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Flujo](#flujo)
  - [Configuración](#configuración)
  - [Ejecución local](#ejecución-local)
  - [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
  - [Pruebas](#pruebas)
  - [Contrato de notificaciones](#contrato-de-notificaciones)

## Por qué existe este componente

RF-007 exige que la verificación de identidad se resuelva de forma asíncrona: `POST /users` responde de inmediato (sin esperar el resultado) y TrueNative notifica el resultado más tarde, llamando a un webhook público/alcanzable que el cliente (nosotros) debe proveer.

Las restricciones de la entrega prohíben ejecutar tareas asíncronas (background tasks, hilos, `asyncio` manual, etc.) dentro de los componentes web de usuarios o tarjetas. Por eso este webhook **no vive dentro de `users_app`**: es un componente totalmente separado que recibe la notificación de TrueNative de forma síncrona (una petición, una respuesta) y delega en `users_app` el único cambio de estado que le corresponde a su dueño de datos.

## Por qué es un contenedor y no un Lambda

La primera versión de este componente se diseñó como función Lambda + API Gateway + SNS. Se descartó por dos razones concretas, no por preferencia:

1. **IAM**: la cuenta de AWS Academy (Learner Lab) no permite crear roles ni políticas IAM nuevas (solo reutilizar `LabRole`, ver `terraform/modules/eks/data.tf`). El Lambda necesitaba su propio rol de ejecución y permisos de `sns:Publish` — no se puede crear ninguno de los dos.
2. **Pasos manuales**: la calificación de la entrega se hace ejecutando los pipelines una sola vez, de forma automática, sobre la cuenta del tutor. El diseño con Lambda requería un paso manual (`kubectl set env` con la URL del Lambda, conocida solo después de que el Lambda ya existe) que el tutor nunca ejecutaría — la entrega no cuenta como manual step más que el de confirmación de correo de SNS que ya documenta el enunciado.

Un contenedor normal, desplegado con el resto de las apps, evita ambos problemas: no necesita IAM (no usa el SDK de AWS en absoluto), y su dirección (`http://identity-webhook-app-service`) es conocida de antemano — no depende de ningún output dinámico de Terraform, así que no hay ciclo de dependencias ni paso manual.

Nota: las tecnologías serverless (Lambda, SNS, SQS) son **opcionales** según el enunciado de la entrega — no hay ningún requisito de que este componente en particular las use. El caso de uso más natural para demostrarlas en este proyecto es el polling de tarjetas de RF-006 (a cargo de otro integrante del equipo), que si necesita genuinamente un componente externo por la restricción de no hacer polling dentro de `credit_cards_app`.

## Requisitos

- Python 3.11
- Poetry 2.1.1
- Docker / Docker Compose

## Estructura del proyecto

```
.
├── src/
│   ├── config.py                     # Settings desde variables de ambiente
│   ├── errors.py
│   ├── signature.py                  # Validación del verifyToken (SHA256)
│   ├── assembly.py                   # Wiring de dependencias (estilo orchestrator_app)
│   ├── domain/
│   │   ├── ports/                    # UsersPort, NotificationsPort
│   │   └── use_cases/                # ProcessVerificationCallbackUseCase
│   ├── adapters/
│   │   └── http/                     # Cliente HTTP con reintentos + adapters concretos
│   └── entrypoints/
│       └── api/
│           ├── main.py               # FastAPI app + manejo de excepciones
│           ├── routers/              # PATCH /verify-callback, GET /ping
│           └── schemas/              # DTO del callback de TrueNative
├── tests/unit/                       # Misma estructura que src/, sin red real
├── Dockerfile
└── pyproject.toml
```

## Flujo

1. TrueNative hace `PATCH /verify-callback` con `{RUV, userIdentifier, createdAt, status, score, verifyToken}`.
2. Se valida `verifyToken` recalculando `sha256("{SECRET_TOKEN}:{RUV}:{SCORE}")`. Si no coincide, se responde 200 igual (TrueNative espera 200 siempre) sin aplicar ningún cambio.
3. Se consulta `GET /users/{userIdentifier}` en `users_app` para obtener el correo y nombre del usuario.
4. Se actualiza el usuario con `PATCH /users/{userIdentifier}` (`status: VERIFICADO | NO_VERIFICADO`).
5. Se notifica el resultado al componente de notificaciones vía HTTP, indiferente del resultado. Si esa llamada falla, se loguea pero no se falla el webhook (el estado del usuario ya quedó aplicado).

## Configuración

Variables de ambiente:

| Variable | Descripción |
|---|---|
| `APP_PORT` | Puerto en el que escucha (default 30007). |
| `TRUE_NATIVE_SECRET_TOKEN` | Mismo `SECRET_TOKEN` configurado en TrueNative, usado para validar la firma del callback. |
| `USERS_APP_BASE_URL` | URL de `users_app` dentro del cluster (`http://users-app-service`). |
| `NOTIFICATIONS_APP_URL` | URL del componente de notificaciones dentro del cluster (`http://notifications-app-service`, pendiente de confirmar el nombre exacto con el equipo). |

## Ejecución local

```bash
poetry install
cp .env.example .env
poetry run uvicorn entrypoints.api.main:app --app-dir src --reload --port 30007
```

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

## Pruebas

```bash
poetry run pytest tests/unit --cov=src --cov-report=term-missing
poetry run ruff check src tests
poetry run black --check src tests
```

Las pruebas unitarias de este componente son opcionales para la calificación de la entrega (según las restricciones), pero se mantienen con 100% de cobertura como estándar del equipo. No requieren red real: el cliente HTTP se mockea con `respx`.

## Contrato de notificaciones

Cuerpo enviado en `POST {NOTIFICATIONS_APP_URL}/notify` (a confirmar con el componente de notificaciones):

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
