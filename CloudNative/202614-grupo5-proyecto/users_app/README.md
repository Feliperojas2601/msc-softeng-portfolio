# Users App

API de gestión de usuarios: creación, actualización, autenticación por token y consulta de identidad. Construida en Python siguiendo arquitectura hexagonal (puertos y adaptadores), igual que el proyecto de ejemplo `pets_app`.

## Tabla de contenido

- [Users App](#users-app)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Requisitos](#requisitos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Configuración](#configuración)
  - [Ejecución local](#ejecución-local)
    - [1. Instalar dependencias](#1-instalar-dependencias)
    - [2. Levantar Postgres](#2-levantar-postgres)
    - [3. Ejecutar la aplicación](#3-ejecutar-la-aplicación)
  - [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
  - [Ejecutar en Docker (imagen suelta)](#ejecutar-en-docker-imagen-suelta)
  - [Ejecutar en Minikube](#ejecutar-en-minikube)
  - [API Endpoints](#api-endpoints)
  - [Modelo de usuario](#modelo-de-usuario)
  - [Pruebas](#pruebas)
    - [Unitarias](#unitarias)
    - [Integración (Postman)](#integración-postman)
  - [Decisiones de seguridad](#decisiones-de-seguridad)
  - [Notas de despliegue](#notas-de-despliegue)

## Requisitos

- Python 3.11
- Poetry 2.1.1
- Docker / Docker Compose
- Minikube / kubectl
- Postman

## Estructura del proyecto

```
.
├── src/
│   ├── domain/
│   │   ├── models/          # Entidad User (Pydantic) y enum UserStatus
│   │   ├── ports/           # UserRepositoryPort (interfaz de persistencia)
│   │   ├── services/        # Hashing de password y generación/expiración de token
│   │   └── use_cases/       # Crear, actualizar, autenticar, consultar, contar, resetear
│   ├── adapters/
│   │   └── database/        # Modelo SQLAlchemy, sesión async, adapter Postgres
│   └── entrypoints/
│       └── api/
│           ├── routers/     # Endpoints REST (prefijo /users)
│           └── schemas/     # DTOs de request/response por endpoint (camelCase)
├── tests/
│   ├── unit/                # Misma estructura que src/, con mocks (sin BD real)
│   └── api/                 # Colección Postman oficial de la entrega
├── Dockerfile                # Build multi-stage, imagen final rootless
├── docker-compose.yml         # App + Postgres para desarrollo local
└── pyproject.toml
```

### Carpeta src

- **domain/models**: entidad `User`, en snake_case, con el enum `UserStatus` (`POR_VERIFICAR`, `NO_VERIFICADO`, `VERIFICADO`).
- **domain/ports**: `UserRepositoryPort`, la interfaz que cualquier adaptador de persistencia debe implementar.
- **domain/services**: `password_service` (hash PBKDF2-SHA256 + salt propio) y `token_service` (generación de UUID4 y cálculo/validación de expiración).
- **domain/use_cases**: un caso de uso por operación de negocio, cada uno recibe el repositorio por inyección de dependencias y no conoce nada de HTTP.
- **adapters/database**: `UserModel` (tabla SQLAlchemy), `session.py` (engine/sesión async y creación de esquema al arrancar) y `SQLAlchemyUserRepositoryAdapter`, la única implementación de `UserRepositoryPort` en esta entrega.
- **entrypoints/api**: `main.py` (app FastAPI, manejo de excepciones, lifespan), `assembly.py` (inyección de dependencias), `routers/user_router.py` (rutas) y `schemas/user_schemas.py` (DTOs con alias camelCase para el contrato HTTP).

## Configuración

Variables de ambiente (ver `.env.example`):

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto donde escucha uvicorn | `30000` |
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `users_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Password de PostgreSQL | `postgres` |
| `TOKEN_EXPIRATION_HOURS` | Horas de validez del token de sesión | `24` |

## Ejecución local

### 1. Instalar dependencias

```bash
poetry install
# Si no existe poetry.lock, ejecute primero:
# poetry lock
```

### 2. Levantar Postgres

```bash
docker run --rm -d --name users_db \
  -e POSTGRES_DB=users_db -e POSTGRES_USER=users_app -e POSTGRES_PASSWORD=users_app \
  -p 5432:5432 postgres:16-alpine
```

### 3. Ejecutar la aplicación

```bash
DB_USER=users_app DB_PASSWORD=users_app \
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 30000
```

El API estará disponible en `http://localhost:30000`. Documentación interactiva: `http://localhost:30000/docs`.

## Ejecutar con Docker Compose

Levanta la aplicación y su base de datos con un solo comando:

```bash
docker compose up --build
```

## Ejecutar en Docker (imagen suelta)

```bash
APP_VERSION=1.0.0
APP_NAME=users_app
docker build --rm --platform linux/amd64 -t ${APP_NAME}:${APP_VERSION} -f Dockerfile --target runner --label version=${APP_VERSION} .
docker run --platform linux/amd64 -p 30000:30000 \
  -e DB_HOST=host.docker.internal -e DB_USER=users_app -e DB_PASSWORD=users_app \
  ${APP_NAME}:${APP_VERSION}
```

## Ejecutar en Minikube

Los manifiestos de despliegue están en [`/k8s/users_app.yaml`](../k8s/users_app.yaml) (Secret, Deployments, Services y NetworkPolicy de `users-app` + `users-db`). Requieren un CNI que aplique `NetworkPolicy` — el CNI por defecto de minikube (kindnet) **no** las aplica, por eso el clúster debe iniciarse con `--cni calico`:

```bash
minikube start --cpus=2 --memory=3g --cni calico

docker build --rm --platform linux/amd64 -t users_app:v1.0.0 -f Dockerfile --target runner --label version=v1.0.0 .
minikube image load users_app:v1.0.0

kubectl apply -f ../k8s/users_app.yaml
kubectl wait --for=condition=ready pod -l app=users-app --timeout=120s

minikube service users-app-service --url
```

Verificación rápida del aislamiento de red (debe imprimir `BLOCKED`, ya que solo `users-app` puede hablar con `users-db`):

```bash
kubectl run netpol-test --rm -i --restart=Never --image=busybox:1.36 --timeout=20s -- \
  sh -c "nc -z -w3 users-db-service 5432 && echo REACHABLE || echo BLOCKED"
```

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/users` | Crea un usuario |
| PATCH | `/users/{id}` | Actualiza `status`, `dni`, `fullName` o `phoneNumber` |
| POST | `/users/auth` | Genera un token de sesión |
| GET | `/users/me` | Retorna el usuario dueño del token (`Authorization: Bearer <token>`) |
| GET | `/users/count` | Cuenta los usuarios almacenados |
| GET | `/users/ping` | Healthcheck |
| POST | `/users/reset` | Elimina todos los usuarios |

## Pruebas

### Unitarias

La estructura de pruebas espeja la de `src/`. Los casos de uso se prueban mockeando `UserRepositoryPort`; el adapter de PostgreSQL se prueba mockeando `AsyncSession` de SQLAlchemy — ninguna prueba unitaria requiere una base de datos real.

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

### Integración (Postman)

La colección ejemplo está en `tests/api/entrega1_users.postman_collection.json`.

## Decisiones de seguridad

- **SQLAlchemy async + asyncpg**, con el esquema creado vía `Base.metadata.create_all()` al arrancar la app.
- **Password**: `pbkdf2_hmac` (SHA-256, 100k iteraciones) con salt propio generado por `secrets.token_hex`.
- **Token**: `uuid4`, vence a las 24h (configurable vía `TOKEN_EXPIRATION_HOURS`). No se usa JWT, según restricción.

## Notas de despliegue

- **`greenlet` como dependencia explícita**: SQLAlchemy async lo requiere en tiempo de ejecución, pero su metadata solo lo activa automáticamente si `platform_machine` es `aarch64`/`x86_64`/etc. En macOS (Apple Silicon) Python reporta `arm64`, un valor que ese marcador no contempla, por lo que `poetry install` lo omite silenciosamente y la app truena al primer request a la base de datos. Se agregó `greenlet` como dependencia directa en `pyproject.toml` para no depender de ese detalle de plataforma.
- **`initContainer` en el Deployment de `users-app`**: sin él, el pod de la app puede arrancar antes que el Service de `users-db` tenga un endpoint listo, causando un `CrashLoopBackOff` inicial (Kubernetes lo recupera solo, pero no es un despliegue limpio). El init container espera a que el puerto 5432 de `users-db-service` responda antes de arrancar el contenedor principal.
- **Minikube requiere `--cni calico`**: el CNI por defecto de minikube no aplica `NetworkPolicy` — los pods pueden hablar entre sí sin restricción aunque el manifiesto esté bien escrito. Verificado localmente: con el CNI por defecto, un pod sin la etiqueta `app=users-app` lograba conectarse a `users-db-service`; con `--cni calico`, la misma prueba queda bloqueada como se espera.