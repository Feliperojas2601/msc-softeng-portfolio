# Offers App

API de ofertas: creación, búsqueda, consulta y eliminación de ofertas asociadas a una publicación. Construida en **Python 3.11** siguiendo una arquitectura hexagonal (puertos y adaptadores).

## Tabla de contenido

- [Requisitos](#requisitos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Ejecución local](#ejecución-local)
- [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
- [Ejecutar en Docker](#ejecutar-en-docker)
- [Ejecutar en Minikube](#ejecutar-en-minikube)
- [API Endpoints](#api-endpoints)
- [Modelo de oferta](#modelo-de-oferta)
- [Pruebas](#pruebas)
- [Decisiones de diseño y seguridad](#decisiones-de-diseño-y-seguridad)
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
│   │   ├── models/          # Entidad Offer
│   │   ├── ports/           # OfferRepositoryPort
│   │   └── use_cases/       # Casos de uso
│   ├── adapters/
│   │   └── database/        # SQLAlchemy y PostgreSQL
│   ├── entrypoints/
│   |   └── api/
│   |       ├── routers/     # Endpoints REST
│   |       └── schemas/     # DTOs
|   ├── assembly.py          # Configuración de dependencias, repositorios y casos de uso
|   ├── config.py            # Configuración y variables de entorno
|   └── errors.py            # Manejo y definición de errores
├── tests/
│   ├── unit/                # Pruebas unitarias, misma estructura que src/, con mocks (sin BD real)
│   └── api/                 # Colección Postman
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### Carpeta `src`

- **`domain/models`**: entidad `Offer` con los campos `id`, `postId`, `userId`, `description`, `size`, `fragile`, `offer` y `createdAt`.
- **`domain/ports`**: interfaz `OfferRepositoryPort` para la persistencia.
- **`domain/use_cases`**: casos de uso de creación, consulta, búsqueda, eliminación, conteo y reseteo.
- **`adapters/database`**: modelo SQLAlchemy, mappers, engine/sesión async, creación de esquema al arrancar y adaptador PostgreSQL.
- **`entrypoints/api`**: aplicación FastAPI, routers y DTOs con campos `camelCase`.
- **`assembly.py`**: configuración de dependencias, repositorios y casos de uso.
- **`config.py`**: configuración de la aplicación y variables de entorno.
- **`errors.py`**: definición y manejo de errores de la aplicación.

## Configuración

Variables de ambiente disponibles en `.env.example`:

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto de la aplicación | `30003` |
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `offers_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `postgres` |

## Ejecución local

### 1. Instalar dependencias

```bash
poetry install
```

### 2. Levantar PostgreSQL

```bash
docker run --rm -d --name offers_db \
  -e POSTGRES_DB=offers_db \
  -e POSTGRES_USER=offers_app \
  -e POSTGRES_PASSWORD=offers_app \
  -p 5432:5432 \
  postgres:16-alpine
```

### 3. Ejecutar la aplicación

```bash
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 30003
```

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

## Ejecutar en Docker

```bash
APP_VERSION=1.0.0
APP_NAME=offers_app

docker build --rm --platform linux/amd64 \
  -t ${APP_NAME}:${APP_VERSION} \
  -f Dockerfile \
  --target runner .

docker run --platform linux/amd64 \
  -p 30003:30003 \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=offers_app \
  -e DB_PASSWORD=offers_app \
  ${APP_NAME}:${APP_VERSION}
```

## Ejecutar en Minikube

Los manifiestos se encuentran en [`k8s/offers_app.yaml`](../k8s/offers_app.yaml).

Se requiere un CNI con soporte para `NetworkPolicy`:

```bash
minikube start --cpus=2 --memory=3g --cni calico
```

### Construir y cargar la imagen

```bash
docker build --rm --platform linux/amd64 \
  -t offers_app:v1.0.0 \
  -f Dockerfile \
  --target runner .

minikube image load offers_app:v1.0.0
```

### Desplegar la aplicación

Desde la carpeta de la aplicación, es decir desde offers_app.

```bash
kubectl apply -f ../k8s/offers_app.yaml

kubectl wait \
  --for=condition=ready pod \
  -l app=offers-app \
  --timeout=120s

minikube service offers-app-service --url
```

### Verificar NetworkPolicy

La siguiente prueba debe responder `BLOCKED`:

```bash
kubectl run netpol-test \
  --rm -i \
  --restart=Never \
  --image=busybox:1.36 \
  --timeout=20s \
  -- sh -c "nc -z -w3 offers-db-service 5432 && echo REACHABLE || echo BLOCKED"
```

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/offers` | Crea una oferta |
| `GET` | `/offers` | Obtiene ofertas y permite filtrar por `post` y `owner` |
| `GET` | `/offers/{id}` | Obtiene una oferta por ID |
| `DELETE` | `/offers/{id}` | Elimina una oferta por ID |
| `GET` | `/offers/count` | Obtiene la cantidad total de ofertas |
| `GET` | `/offers/ping` | Health check |
| `POST` | `/offers/reset` | Elimina todas las ofertas |

## Modelo de oferta

### Crear oferta

El endpoint `POST /offers` recibe un objeto `CreateOffer`:

```json
{
  "postId": "9c858901-8a57-4791-81fe-4c455b099bc9",
  "userId": "b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11",
  "description": "Paquete pequeño con libros",
  "size": "SMALL",
  "fragile": false,
  "offer": 25.5
}
```

`size` debe ser `LARGE`, `MEDIUM` o `SMALL` y `offer` no puede ser negativo; de lo contrario la API responde `412`.

### Respuesta de creación

```json
{
  "id": "a3f1c2d4-0000-4000-8000-000000000001",
  "userId": "b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11",
  "createdAt": "2026-08-20T19:40:00Z"
}
```

### Consulta y búsqueda

Al consultar una oferta por ID o al listarlas, la API retorna el objeto completo:

```json
{
  "id": "a3f1c2d4-0000-4000-8000-000000000001",
  "postId": "9c858901-8a57-4791-81fe-4c455b099bc9",
  "userId": "b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11",
  "description": "Paquete pequeño con libros",
  "size": "SMALL",
  "fragile": false,
  "offer": 25.5,
  "createdAt": "2026-08-20T19:40:00Z"
}
```

## Pruebas

### Unitarias

Los casos de uso se prueban de forma aislada utilizando mocks de `OfferRepositoryPort`.

```bash
poetry install

poetry run pytest \
  --cov=src \
  -v -s \
  --cov-fail-under=70 \
  --cov-report term-missing
```

### Integración

La colección de Postman se encuentra en:

```text
tests/api/offers.postman_collection.json
```

## Decisiones de diseño y seguridad

- **Arquitectura hexagonal:** separa dominio, casos de uso, persistencia y API.
- **Validación en dos niveles:** campos ausentes o mal tipados responden `400` (vía `RequestValidationError`); reglas de negocio como `size` inválido u `offer` negativo responden `412` (vía `InvalidOfferError`).
- **Fechas UTC:** se utilizan fechas ISO 8601 con `timezone.utc` y `DateTime(timezone=True)`.
- **Persistencia segura:** SQLAlchemy ORM y `asyncpg` gestionan las consultas evitando SQL construido manualmente.
- **Health checks:** Kubernetes utiliza `/offers/ping` para verificar el estado del servicio.

## Notas de despliegue

- **Init container:** Kubernetes espera a que PostgreSQL esté disponible antes de iniciar `offers-app`.
- **NetworkPolicy:** restringe el acceso directo a PostgreSQL desde otros pods.
- **Minikube:** `imagePullPolicy: IfNotPresent` permite utilizar la imagen cargada localmente sin descargarla de Docker Hub.
