# Routes App

API REST para crear, consultar, filtrar y eliminar trayectos. Está construida con
FastAPI, PostgreSQL y SQLAlchemy asíncrono mediante arquitectura hexagonal.

## Arquitectura

```text
src/
├── domain/
│   ├── models/          # Route y catálogo AirportCode
│   ├── ports/           # Contrato RoutesRepositoryPort
│   └── use_cases/       # Reglas de negocio por operación
├── adapters/database/   # SQLAlchemy, sesión async y repositorio PostgreSQL
├── entrypoints/api/
│   ├── routers/         # Los siete endpoints bajo /routes
│   ├── schemas/         # DTO de entrada y salida en camelCase
│   └── main.py          # FastAPI, lifespan y handlers de errores
├── assembly.py          # Inyección de dependencias
└── config.py            # Variables de entorno
```

La dirección de las dependencias es `API -> casos de uso -> puerto`. El adaptador
de PostgreSQL implementa el puerto y se inyecta desde `assembly.py`; por eso la
lógica de negocio no depende de FastAPI ni de SQLAlchemy.

## Requisitos

- Python 3.11
- Poetry 2.1.1
- Docker y Docker Compose
- Mínimo 4 GB de RAM y 2 cores para el entorno local de Minikube

## Variables de entorno

| Variable | Valor local predeterminado |
|---|---:|
| `APP_PORT` | `30002` |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `routes_db` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | `postgres` |

Puede crear un archivo `.env` a partir de `.env.example` si va a ejecutar la API
fuera de Docker.

## Ejecución con Docker Compose

Desde esta carpeta:

```powershell
docker compose up --build
```

Esto crea dos contenedores independientes:

- `routes_app`: API en `http://localhost:30002`.
- `routes_db`: PostgreSQL, publicado en el puerto local obligatorio `5432`.

La documentación Swagger queda en `http://localhost:30002/docs`. Para detenerlos:

```powershell
docker compose down
```

## Ejecución local

Primero instale las dependencias y levante PostgreSQL:

```powershell
poetry lock
poetry install
docker compose up -d routes_db
```

Como PostgreSQL se publica localmente por el puerto `5432`, ejecute Uvicorn con
la configuración predeterminada:

```powershell
poetry run uvicorn entrypoints.api.main:app --app-dir src --reload --port 30002
```

## Endpoints

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/routes` | Crea un trayecto (`201`) |
| `GET` | `/routes` | Lista todos los trayectos |
| `GET` | `/routes?flight={flightId}` | Filtra por identificador de vuelo |
| `GET` | `/routes/{id}` | Consulta un trayecto por UUID |
| `DELETE` | `/routes/{id}` | Elimina un trayecto |
| `GET` | `/routes/count` | Retorna `{"count": n}` |
| `GET` | `/routes/ping` | Retorna `pong` |
| `POST` | `/routes/reset` | Elimina todos los trayectos |

Ejemplo de creación:

```json
{
  "flightId": "AV-001",
  "sourceAirportCode": "BOG",
  "sourceCountry": "Colombia",
  "destinyAirportCode": "MEX",
  "destinyCountry": "México",
  "bagCost": 120,
  "plannedStartDate": "2099-01-01T10:00:00",
  "plannedEndDate": "2099-01-01T14:00:00"
}
```

Reglas relevantes:

- `flightId` es único.
- Ambos aeropuertos deben pertenecer al enum `AirportCode`.
- `bagCost` debe ser cero o positivo.
- Las fechas deben ser futuras y la fecha final debe ser posterior a la inicial.
- Los campos HTTP usan `camelCase`; internamente el dominio usa `snake_case`.

## Pruebas y calidad

```powershell
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
poetry run black --check .
poetry run isort --check . --profile black
poetry run bandit -c pyproject.toml -r .
poetry run ruff check
```

Desde la raíz del repositorio también puede usar:

```powershell
make unittest DIR=routes_app
make lintcheck DIR=routes_app
```

## Kubernetes

El manifiesto `../k8s/routes_app.yaml` contiene Secret, Deployments, Services,
sondas de salud, límites de recursos y una `NetworkPolicy` que permite que solo
`routes_app` acceda a `routes_db`.

La aplicación escucha en el puerto `30002` dentro del pod y el Service la
publica fuera del clúster mediante el `NodePort` `30002`.

```powershell
minikube start --cpus=2 --memory=4g --cni calico
docker build -t routes_app:v1.0.0 .
minikube image load routes_app:v1.0.0
kubectl apply -f ../k8s/routes_app.yaml
```
