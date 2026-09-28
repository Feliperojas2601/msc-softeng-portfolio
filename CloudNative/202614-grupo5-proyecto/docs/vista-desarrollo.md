# Vista de desarrollo

[← Volver al inicio](./README.md)

La [estructura de desarrollo de RF-006](./requerimientos/rf-006.md#estructura-de-desarrollo) distingue la API síncrona de tarjetas y la Lambda externa de polling. Su [configuración de despliegue](./requerimientos/rf-006.md#configuración-declarativa) describe cómo activar el componente cuando exista un execution role autorizado.

## Tabla de contenido

- [Vista de desarrollo](#vista-de-desarrollo)
  - [Introducción](#introducción)
  - [Estructura de carpetas del proyecto](#estructura-de-carpetas-del-proyecto)
  - [Estructura de carpetas de una aplicación](#estructura-de-carpetas-de-una-aplicación)
  - [Tabla de tecnologías](#tabla-de-tecnologías)

## Introducción

Esta vista describe las decisiones de desarrollo del proyecto: cómo está organizado el código y qué herramientas se usan en cada etapa (desarrollo, ejecución, pruebas y despliegue).

## Estructura de carpetas del proyecto

El proyecto sigue una estrategia de monorepo: un único repositorio de GitHub contiene el código fuente de todas las aplicaciones, cada una en su propia carpeta y sin acoplamiento entre ellas.

```
.
├── .github/workflows/   # Pipelines de evaluación del curso (no se modifican, salvo ci_evaluador_unit.yml)
├── k8s/                 # Manifiestos de despliegue en Kubernetes, un archivo por aplicación
├── docs/                # Documentación técnica (este sitio) y sus diagramas PlantUML
├── users_app/            # Aplicación de gestión de usuarios
├── posts_app/            # Aplicación de gestión de publicaciones
├── offers_app/           # Aplicación de gestión de ofertas
├── routes_app/           # Aplicación de gestión de trayectos
├── orchestrator_app/     # Orquestación de los requerimientos RF-003, RF-004 y RF-005
├── scores_app/           # Cálculo y persistencia de la utilidad de las ofertas
├── terraform/            # Infraestructura AWS declarada como código
├── config.yaml           # Configuración del equipo y de cada aplicación, usada por los pipelines
├── makefile               # Reglas compartidas de lint y pruebas unitarias, usadas por los pipelines
└── README.md              # Estructura del repositorio y guía de despliegue completo
```

## Estructura de carpetas de una aplicación

Cada aplicación en Python sigue una arquitectura hexagonal (puertos y adaptadores), tal como se implementó en `users_app`:

```
<aplicación>/
├── src/
│   ├── domain/
│   │   ├── models/       # Entidades de dominio (Pydantic)
│   │   ├── ports/        # Interfaces de persistencia (Repository)
│   │   ├── services/     # Lógica de negocio sin dependencias externas (hashing, tokens, etc.)
│   │   └── use_cases/    # Casos de uso, un archivo por operación de negocio
│   ├── adapters/
│   │   └── database/     # Implementación de los puertos contra PostgreSQL (SQLAlchemy)
│   └── entrypoints/
│       └── api/           # Aplicación FastAPI, routers y esquemas de request/response
├── tests/
│   ├── unit/               # Pruebas unitarias, misma estructura que src/
│   └── api/                 # Colección Postman de pruebas de integración
├── Dockerfile               # Build multi-stage, imagen final rootless
├── docker-compose.yml       # Aplicación + base de datos para desarrollo local
└── pyproject.toml           # Dependencias y configuración de linters/pruebas (Poetry)
```

Esta separación permite que la lógica de negocio (`domain`) no dependa de FastAPI ni de SQLAlchemy: los casos de uso reciben el repositorio por inyección de dependencias (`assembly.py`) y solo conocen la interfaz definida en `domain/ports`, no su implementación concreta.

## Tabla de tecnologías

| Etapa | Herramienta | Descripción |
|---|---|---|
| Desarrollo | Python 3.11, Poetry, FastAPI, Pydantic | Lenguaje, gestor de dependencias y framework web de cada aplicación |
| Linters | Black, isort, Ruff, Bandit | Formato, orden de imports, estilo y análisis de seguridad estático |
| Pruebas unitarias | Pytest, pytest-cov, pytest-mock, pytest-asyncio | Ejecución de pruebas, cobertura (mínimo 70%) y mocks de dependencias asíncronas |
| Pruebas de integración | Postman, Newman | Validación del contrato de API de cada aplicación |
| Ejecución local | Docker, Docker Compose | Contenedores de aplicación y bases locales para desarrollo y pruebas |
| Despliegue local | Kubernetes, Minikube, kubectl | Validación opcional de los manifiestos en un clúster local |
| Despliegue en la nube | Kubernetes, AWS EKS, Terraform | Entorno evaluado: aplicaciones contenerizadas en EKS e infraestructura aprovisionada con Terraform |
| Base de datos en la nube | PostgreSQL 16 en AWS RDS | Una única base física `clonatdevs`, con tablas lógicamente desacopladas por dominio, accesible por el puerto 5432 |
| Integración continua | GitHub Actions | Linters, pruebas unitarias y validación de despliegue en cada push/PR |
| Documentación | Markdown, PlantUML, Vale | Documentación versionada como código y su revisión gramatical automática |
