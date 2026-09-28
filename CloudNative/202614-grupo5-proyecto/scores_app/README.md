# Scores App

API de scores: calcula y persiste la utilidad (score) de una oferta. Construida en **Python 3.11** siguiendo una arquitectura hexagonal (puertos y adaptadores), igual que el resto de aplicaciones del sistema.

## Tabla de contenido

- [Requisitos](#requisitos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Ejecución local](#ejecución-local)
- [Ejecutar con Docker Compose](#ejecutar-con-docker-compose)
- [Ejecutar en Minikube](#ejecutar-en-minikube)
- [API Endpoints](#api-endpoints)
- [Modelo de score](#modelo-de-score)
- [Pruebas](#pruebas)
- [Decisiones de diseño](#decisiones-de-diseño)

## Requisitos

- Python 3.11
- Poetry 2.1.1
- Docker / Docker Compose
- Minikube / kubectl

## Estructura del proyecto

```
.
├── src/
│   ├── domain/
│   │   ├── models/          # Entidad Score
│   │   ├── ports/           # ScoreRepositoryPort
│   │   └── use_cases/       # CreateScoreUseCase, GetScoreUseCase
│   ├── adapters/
│   │   └── database/        # SQLAlchemy y PostgreSQL
│   ├── entrypoints/
│   │   └── api/
│   │       ├── routers/     # Endpoints REST
│   │       └── schemas/     # DTOs
│   ├── assembly.py          # Configuración de dependencias, repositorios y casos de uso
│   ├── config.py            # Configuración y variables de entorno
│   └── errors.py            # Manejo y definición de errores
├── tests/
│   └── unit/                # Pruebas unitarias, misma estructura que src/, con mocks (sin BD real)
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### Carpeta `src`

- **`domain/models`**: entidad `Score` con los campos `id`, `offerId`, `size`, `offer`, `bagCost`, `utility` y `createdAt`.
- **`domain/ports`**: interfaz `ScoreRepositoryPort` para la persistencia.
- **`domain/use_cases`**: `CreateScoreUseCase` (aplica la fórmula de la utilidad) y `GetScoreUseCase` (consulta por oferta).
- **`adapters/database`**: modelo SQLAlchemy, mappers, engine/sesión async, creación de esquema al arrancar y adaptador PostgreSQL.
- **`entrypoints/api`**: aplicación FastAPI, router y DTOs.
- **`assembly.py`**: configuración de dependencias, repositorios y casos de uso.
- **`config.py`**: configuración de la aplicación y variables de entorno.
- **`errors.py`**: definición y manejo de errores de la aplicación.

## Configuración

Variables de ambiente disponibles en `.env.example`:

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto de la aplicación | `30004` |
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `scores_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `postgres` |

## Ejecución local

### 1. Instalar dependencias

```bash
poetry install
```

### 2. Levantar PostgreSQL

```bash
docker run --rm -d --name scores_db \
  -e POSTGRES_DB=scores_db \
  -e POSTGRES_USER=scores_app \
  -e POSTGRES_PASSWORD=scores_app \
  -p 5432:5432 \
  postgres:16-alpine
```

### 3. Ejecutar la aplicación

```bash
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 30004
```

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

## Ejecutar en Minikube

Los manifiestos se encuentran en [`k8s/scores_app.yaml`](../k8s/scores_app.yaml).

```bash
docker build --rm --platform linux/amd64 \
  -t scores_app:v1.0.0 \
  -f Dockerfile \
  --target runner .

minikube image load scores_app:v1.0.0

kubectl apply -f ../k8s/scores_app.yaml

kubectl wait \
  --for=condition=ready pod \
  -l app=scores-app \
  --timeout=120s

minikube service scores-app-service --url
```

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/scores` | Calcula y persiste la utilidad de una oferta |
| `GET` | `/scores/{offerId}` | Obtiene el score de una oferta; `404` si aún no se ha calculado |
| `GET` | `/scores/ping` | Health check |

## Modelo de score

### Crear score

El endpoint `POST /scores` recibe:

```json
{
  "offerId": "9c858901-8a57-4791-81fe-4c455b099bc9",
  "size": "MEDIUM",
  "offer": 100.0,
  "bagCost": 20.0
}
```

`size` debe ser `LARGE`, `MEDIUM` o `SMALL`; de lo contrario la API responde `412`.

### Respuesta

```json
{
  "id": "a3f1c2d4-0000-4000-8000-000000000001",
  "offerId": "9c858901-8a57-4791-81fe-4c455b099bc9",
  "size": "MEDIUM",
  "offer": 100.0,
  "bagCost": 20.0,
  "utility": 90.0,
  "createdAt": "2026-09-04T03:17:20.019138+00:00"
}
```

## Pruebas

```bash
poetry run pytest -q
```

## Decisiones de diseño

- **Fórmula de la utilidad.** `utility = offer - (ocupación(size) * bagCost)`, con ocupación `LARGE` 100 %, `MEDIUM` 50 % y `SMALL` 25 %. La fórmula y su persistencia viven únicamente aquí; `orchestrator_app` solo envía las entradas.
- **Sin integraciones salientes.** `scores_app` no consulta a otros servicios de dominio: recibe todas las entradas necesarias en la petición.
- **Resiliencia ante score no definido.** `GET /scores/{offerId}` responde `404` cuando la oferta aún no tiene score calculado, en vez de fallar. Los consumidores (por ejemplo, futuras consultas agregadas de ofertas) deben tratar esa ausencia como un estado válido, no como un error.
- **Persistencia propia.** El score se almacena en su propia base de datos (`scores_db`) porque puede cambiar en el tiempo; no es un cálculo efímero.
