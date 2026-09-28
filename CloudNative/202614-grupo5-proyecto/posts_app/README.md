# Posts App

API de gestión de publicaciones: creación, consulta, expiración y filtrado. Construida en **Python 3.13** siguiendo una arquitectura hexagonal (puertos y adaptadores).

## Tabla de contenido

- [Requisitos](#requisitos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Ejecución local](#ejecución-local)
- [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
- [Ejecutar en Docker](#ejecutar-en-docker)
- [Ejecutar en Minikube](#ejecutar-en-minikube)
- [API Endpoints](#api-endpoints)
- [Modelo de publicación](#modelo-de-publicación)
- [Pruebas](#pruebas)
- [Decisiones de diseño y seguridad](#decisiones-de-diseño-y-seguridad)
- [Notas de despliegue](#notas-de-despliegue)

## Requisitos

- Python 3.13
- Poetry 2.1.1
- Docker / Docker Compose
- Minikube / kubectl
- Postman

## Estructura del proyecto

```
.
├── src/
│   ├── domain/
│   │   ├── models/          # Entidad Post
│   │   ├── ports/           # PostRepositoryPort
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

- **`domain/models`**: entidad `Post` con los campos `id`, `routeId`, `userId`, `expireAt` y `createdAt`.
- **`domain/ports`**: interfaz `PostRepositoryPort` para la persistencia.
- **`domain/use_cases`**: casos de uso de creación, consulta, expiración, conteo y reseteo.
- **`adapters/database`**: modelo SQLAlchemy, mappers, engine/sesión async y creación de esquema al arrancar y adaptador PostgreSQL.
- **`entrypoints/api`**: aplicación FastAPI, routers y DTOs con campos `camelCase`.
- **`assembly.py`**: configuración de dependencias, repositorios y casos de uso.
- **`config.py`**: configuración de la aplicación y variables de entorno.
- **`errors.py`**: definición y manejo de errores de la aplicación.

## Configuración

Variables de ambiente disponibles en `.env.example`:

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto de la aplicación | `30001` |
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `posts_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `postgres` |

## Ejecución local

### 1. Instalar dependencias

```bash
poetry install
```

### 2. Levantar PostgreSQL

```bash
docker run --rm -d --name posts_db \
  -e POSTGRES_DB=posts_db \
  -e POSTGRES_USER=posts_app \
  -e POSTGRES_PASSWORD=posts_app \
  -p 5432:5432 \
  postgres:16-alpine
```

### 3. Ejecutar la aplicación

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

## Ejecutar en Docker

```bash
APP_VERSION=1.0.0
APP_NAME=posts_app

docker build --rm --platform linux/amd64 \
  -t ${APP_NAME}:${APP_VERSION} \
  -f Dockerfile \
  --target runner .

docker run --platform linux/amd64 \
  -p 30001:30001 \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=posts_app \
  -e DB_PASSWORD=posts_app \
  ${APP_NAME}:${APP_VERSION}
```

## Ejecutar en Minikube

Los manifiestos se encuentran en [`k8s/posts_app.yaml`](../k8s/posts_app.yaml).

Se requiere un CNI con soporte para `NetworkPolicy`:

```bash
minikube start --cpus=2 --memory=3g --cni calico
```

### Construir y cargar la imagen

```bash
docker build --rm --platform linux/amd64 \
  -t posts_app:v1.0.0 \
  -f Dockerfile \
  --target runner .

minikube image load posts_app:v1.0.0
```

### Desplegar la aplicación
Desde la carpeta de la aplicación, es decir desde posts_app.

```bash
kubectl apply -f ../k8s/posts_app.yaml

kubectl wait \
  --for=condition=ready pod \
  -l app=posts-app \
  --timeout=120s

minikube service posts-app-service --url
```

### Verificar NetworkPolicy

La siguiente prueba debe responder `BLOCKED`:

```bash
kubectl run netpol-test \
  --rm -i \
  --restart=Never \
  --image=busybox:1.36 \
  --timeout=20s \
  -- sh -c "nc -z -w3 posts-db-service 5432 && echo REACHABLE || echo BLOCKED"
```

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/posts` | Crea una publicación |
| `GET` | `/posts` | Obtiene publicaciones y permite filtrar por `expire`, `route` y `owner` |
| `GET` | `/posts/{id}` | Obtiene una publicación por ID |
| `DELETE` | `/posts/{id}` | Elimina una publicación por ID |
| `GET` | `/posts/count` | Obtiene la cantidad total de publicaciones |
| `GET` | `/posts/ping` | Health check |
| `POST` | `/posts/reset` | Elimina todas las publicaciones |


## Modelo de publicación

### Crear publicación

El endpoint `POST /posts/` recibe un objeto `CreatePost`:

```json
{
  "routeId": "a1b2c3d4-1111-4000-8000-000000000001",
  "userId": "b2c3d4e5-2222-4000-8000-000000000002",
  "expireAt": "2026-08-27T19:40:00Z"
}
```

### Respuesta

Al crear o consultar una publicación, la API retorna un objeto `PostResponse`:

```json
{
  "id": "a3f1c2d4-0000-4000-8000-000000000001",
  "userId": "b2c3d4e5-2222-4000-8000-000000000002",
  "createdAt": "2026-08-20T19:40:00Z"
}
```

## Pruebas

### Unitarias

Los casos de uso se prueban de forma aislada utilizando mocks de `PostRepositoryPort`.

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
tests/api/entrega1_posts_postman.json
```

## Decisiones de diseño y seguridad

- **Arquitectura hexagonal:** separa dominio, casos de uso, persistencia y API.
- **Fechas UTC:** se utilizan fechas ISO 8601 con `timezone.utc` y `DateTime(timezone=True)`.
- **Persistencia segura:** SQLAlchemy ORM y `asyncpg` gestionan las consultas evitando SQL construido manualmente.
- **Health checks:** Kubernetes utiliza `/posts/ping` para verificar el estado del servicio.

## Notas de despliegue

- **Init container:** Kubernetes espera a que PostgreSQL esté disponible antes de iniciar `posts-app`.
- **NetworkPolicy:** restringe el acceso directo a PostgreSQL desde otros pods.
- **Minikube:** `imagePullPolicy: IfNotPresent` permite utilizar la imagen cargada localmente sin descargarla de Docker Hub.
