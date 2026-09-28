# Credit Cards App

Componente síncrono responsable del API de tarjetas de crédito bajo `/credit-cards`.

Implementa el listado autenticado, los endpoints de soporte de la tarea #244 y la creación síncrona de la historia #243. Utiliza Flask, SQLAlchemy, psycopg y HTTPX síncronos. No ejecuta polling, hilos ni tareas en segundo plano. El worker en contenedor (no Lambda) de `credit_cards_mediator_app` realiza la verificación posterior mediante el endpoint interno idempotente.

## API implementada

| Método | Ruta | Autenticación | Respuesta |
|---|---|---|---|
| GET | `/credit-cards` | Bearer validado mediante `GET /users/me` | `200`: arreglo de tarjetas del usuario; `[]` si no tiene tarjetas. |
| GET | `/credit-cards/count` | No requiere | `200`: `{"count": 0}` con el total real de tarjetas de todos los usuarios. |
| GET | `/credit-cards/ping` | No requiere | `200`: texto `pong`, sin consultar usuarios ni base de datos. |
| POST | `/credit-cards/reset` | No requiere, según contrato académico | `200`: `{"msg": "Todos los datos fueron eliminados"}`. Elimina todas las tarjetas, sin borrar tablas de otros componentes. |
| POST | `/credit-cards` | Bearer validado mediante `GET /users/me` | `201`: `id`, `userId` y `createdAt`. Registra la tarjeta en TrueNative y persiste solo el token, últimos cuatro dígitos, franquicia y estado `POR_VERIFICAR`. |
| GET | `/credit-cards/internal/{cardId}/verification` | Bearer de servicio `CREDIT_CARDS_INTERNAL_SECRET` | `200`: `id`, `userId`, `ruv`, `status`, `lastFourDigits`, `franchise` y `updatedAt`; `404` si no existe. No devuelve token de pagos. |
| PATCH | `/credit-cards/internal/{cardId}/verification` | Bearer de servicio `CREDIT_CARDS_INTERNAL_SECRET` | `200`: los mismos datos del GET interno después de finalizar. Solo permite finalizar desde `POR_VERIFICAR`; repetir el mismo estado no cambia `updatedAt`. |

El listado contiene exactamente `id`, `token`, `userId`, `lastFourDigits`, `issuer`, `status`, `createdAt` y `updatedAt`. El token de pagos se incluye exclusivamente por exigencia educativa del contrato. Las fechas se serializan en UTC como `yyyy-mm-ddTHH:MM:SS`. No se retorna RUV ni información completa de la tarjeta. El propietario se obtiene del servicio de usuarios; parámetros como `userId` no permiten consultar tarjetas ajenas.

El listado responde `403` con cuerpo vacío cuando no hay token, y `401` con cuerpo vacío ante credenciales malformadas o rechazadas por usuarios. `users_app` es responsable de validar expiración y estado verificado. Ante una falla de transporte, respuesta inválida de usuarios o fallo de base de datos, se responde `503` vacío, sin divulgar detalles internos. No se reintenta automáticamente ni se siguen redirecciones al reenviar el Bearer.

La creación valida `cardNumber` numérico sin espacios, `cvv` de 3 o 4 dígitos, `expirationDate` con `YY/MM` y `cardHolderName` no vacío. Responde `403` sin token, `401` con token inválido o vencido, `400` ante formato inválido o rechazo del proveedor, `409` ante duplicado y `412` ante tarjeta vencida. El límite de TrueNative y usuarios es de 2 segundos cada uno para conservar el presupuesto total de 5 segundos; la persistencia es local y síncrona.

`reset` es global e idempotente, conforme al API de evaluación.

El worker reclama un evento por llamada a
`POST /credit-cards/internal/verification-events/claim`, con una reserva de
60 segundos. Cuando TrueNative responde `202`, llama a
`POST /credit-cards/internal/verification-events/{eventId}/release` con
`{"leaseId": "..."}` y Bearer de servicio. La API valida la reserva vigente,
la libera y reprograma el evento para un segundo después; responde
`200 {"scheduled": true}` o `409` si la reserva no corresponde.
El endpoint `ack` confirma únicamente eventos completados por el worker.

## Ejecución local

```bash
cp .env.example .env
poetry install
PYTHONPATH=src poetry run python -m entrypoints.api.main
```

El healthcheck está disponible en `http://localhost:30006/credit-cards/ping`.

Se requiere Python 3.13. En PowerShell, establecer `$env:PYTHONPATH="src"` antes de ejecutar `poetry run python -m entrypoints.api.main`. Al iniciar mediante ese comando se crean las tablas propias; PostgreSQL debe estar disponible. La importación de la fábrica de aplicación no conecta a la base ni crea tablas.

| Variable | Uso |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Conexión a la base exclusiva de tarjetas. El ejemplo local usa el puerto 5436 publicado por Compose. |
| `USERS_APP_URL` | URL base de usuarios, sin `/users/me`. Local: `http://localhost:30000`; EKS: `http://users-app-service`. |
| `USERS_TIMEOUT_SECONDS` | Timeout HTTP positivo, por defecto 2 segundos. |
| `CREDIT_CARDS_INTERNAL_SECRET` | Token de servicio usado por `credit_cards_mediator_app` para finalizar la verificación. |

## Docker

```bash
docker compose up --build
```

Compose espera a que PostgreSQL esté saludable antes de iniciar la aplicación. No despliega `users_app`: debe ejecutarse por separado. Desde el contenedor en Docker Desktop, configurar `USERS_APP_URL=http://host.docker.internal:30000`; una URL con `localhost` dentro del contenedor apuntaría al propio contenedor. El listado necesita usuarios, mientras que count, ping y reset no lo consultan.

## Pruebas

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=70
poetry run ruff check .
poetry run ruff format --check .
```

Las pruebas usan una base SQLite aislada y simulan HTTP de usuarios. Cubren el contrato de respuesta, filtrado por propietario, estados, autenticación, fallos de dependencias, count global, reset idempotente, conservación de otras tablas y fechas UTC. No ejecutan reset sobre una base desplegada. La integración real con PostgreSQL y usuarios debe validarse adicionalmente en el entorno de despliegue.
