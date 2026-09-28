# Orchestrator App

Orquestador de los requerimientos compuestos de la Entrega 2 (RF-003, RF-004,
RF-005). El cliente hace **una sola** petición HTTP por requerimiento y este
componente coordina a `users_app`, `posts_app`, `offers_app`, `routes_app` y
`scores_app` para completarlo, manteniendo la consistencia de los datos.

**Fuera de alcance:** no persiste datos propios, no reimplementa reglas que ya
viven en los servicios de dominio, y no enruta el tráfico de paso
(`/users/*`, `/posts/*`, `/offers/*`, `/routes/*`) — de eso se encarga el Ingress.

## Tabla de contenido

- [Arquitectura](#arquitectura)
- [Capacidades / API](#capacidades--api)
- [Configuración](#configuración)
- [Ejecución local](#ejecución-local)
- [Despliegue en Kubernetes](#despliegue-en-kubernetes)
- [Pruebas](#pruebas)
- [Decisiones de diseño](#decisiones-de-diseño)

## Arquitectura

- **Tipo:** orquestador (BFF sin estado) sobre los microservicios de dominio.
- **Stack:** Python 3.11, FastAPI, `httpx` como cliente HTTP saliente, Poetry.
- **Estilo:** arquitectura hexagonal (puertos y adaptadores), igual que el resto
  del repositorio.
  - `src/domain/models` — modelos del dominio (`Caller`, `Post`, `CreatedOffer`,
    `CreateOfferCommand`).
  - `src/domain/ports` — contratos de acceso a usuarios, publicaciones, trayectos, ofertas y scores.
  - `src/domain/use_cases` — casos de uso de RF-003, RF-004 y RF-005.
  - `src/adapters/http` — implementaciones `httpx` de los puertos, incluido el adaptador real de
    Scores. `client.py` centraliza timeout, reintentos y parseo de fechas.
  - `src/entrypoints/api` — routers, schemas y manejadores de excepción.
  - `src/assembly.py` — inyección de dependencias (FastAPI `Depends`).
- **Patrones:** orquestación síncrona con **acción compensatoria** (saga) para
  RF-004; el orquestador es el único punto donde se decide el orden de las
  llamadas y cómo revertir ante un fallo parcial.

### Dependencias

| Servicio | Uso |
|---|---|
| `users_app` | `GET /users/me` — valida el token y resuelve el usuario de la sesión. |
| `posts_app` | `GET /posts/{id}` — obtiene la publicación objetivo. |
| `routes_app` | `GET /routes/{id}` — costo de maleta (RF-004) o trayecto completo (RF-005). |
| `offers_app` | `POST /offers` — crea la oferta; `DELETE /offers/{id}` — compensación; `GET /offers?post={id}` — ofertas de una publicación (RF-005). |
| `scores_app` | `POST /scores` — cálculo y persistencia de la utilidad; `GET /scores/{offerId}` — utilidad ya calculada (RF-005). |

## Capacidades / API

| Método | Ruta | Descripción | Estado |
|---|---|---|---|
| `POST` | `/rf004/posts/{id}/offers` | RF-004: crea una oferta sobre una publicación. | Implementado. |
| `GET` | `/ping` | Healthcheck. | Implementado |
| `POST` | `/rf003/posts` | RF-003: crear publicaciones. | Implementado. |
| `GET` | `/rf005/posts/{id}` | RF-005: consultar publicación con ofertas. | Implementado. |

### RF-004 — flujo y códigos de error

1. Cuerpo mal formado / campo faltante / `size` fuera de `{LARGE, MEDIUM, SMALL}` → **400**.
2. Sin header `Authorization` → **403**.
3. Token inválido o vencido (`GET /users/me`) → **401**.
4. La publicación no existe (`GET /posts/{id}`) → **404**.
5. La publicación ya expiró (`expireAt <= ahora`, UTC) → **412**.
6. La publicación es del mismo usuario → **412**.
7. `POST /offers`; luego `ScorePort.create_score(...)` contra `scores_app`. Si el
   paso de score falla, se compensa con `DELETE /offers/{id}` y se responde **503**.
8. Cualquier fallo o timeout de un servicio → **503**
   (`{"msg": "El servicio está temporalmente fuera de servicio."}`).
9. Éxito → **201**
   `{"data": {"id", "userId", "createdAt", "postId"}, "msg": "<resumen>"}`.

### RF-005 — flujo y códigos de error

1. Sin header `Authorization` → **403**.
2. Token inválido o vencido (`GET /users/me`) → **401**.
3. La publicación no existe (`GET /posts/{id}`) → **404**.
4. El caller no es el dueño de la publicación → **403**.
5. `GET /routes/{routeId}` (trayecto completo) y `GET /offers?post={id}` (ofertas).
   Un fallo o timeout en cualquiera de los dos → **503**.
6. Por cada oferta, `ScorePort.get_score(offerId)` contra `scores_app`. A diferencia
   del resto de llamadas, **nunca** propaga un error: si falla, no responde o no
   tiene el score (404), esa oferta queda con `score: null` sin afectar el resto
   de la respuesta (degradación con gracia).
7. Las ofertas se ordenan descendente por `score` (las `null` quedan al final).
8. Éxito → **200** con la publicación, el trayecto y las ofertas ordenadas.

## Configuración

| Variable | Descripción | Default |
|---|---|---|
| `APP_PORT` | Puerto en el que escucha el servicio. | `30005` |
| `USERS_APP_URL` | URL base de `users_app`. | `http://localhost:30000` |
| `POSTS_APP_URL` | URL base de `posts_app`. | `http://localhost:30001` |
| `ROUTES_APP_URL` | URL base de `routes_app`. | `http://localhost:30002` |
| `OFFERS_APP_URL` | URL base de `offers_app`. | `http://localhost:30003` |
| `SCORES_APP_URL` | URL base de `scores_app`. | `http://localhost:30004` |
| `HTTP_TIMEOUT_SECONDS` | Timeout por llamada saliente. | `3.0` |
| `HTTP_MAX_RETRIES` | Reintentos extra, **solo** en llamadas GET. | `1` |

## Ejecución local

Requiere que los servicios de dominio estén corriendo en los puertos indicados.

```bash
cd orchestrator_app
cp .env.example .env
poetry install
poetry run uvicorn entrypoints.api.main:app --app-dir src --port 30005
```

Con Docker:

```bash
docker compose up --build
```

## Despliegue en Kubernetes

Manifiesto: [`k8s/aws/orchestrator_app.yml`](../k8s/aws/orchestrator_app.yml)
(`Deployment` + `Service` ClusterIP). Sin base de datos: solo consume por HTTP los `Service` de los servicios de dominio.
Los manifiestos AWS de esos servicios están junto a este, en `k8s/aws/`; los de `k8s/` son el despliegue local deprecados.

`k8s/aws/ingress.yml` publica el host único: `/rf003`, `/rf004`, `/rf005` van al orquestador y `/users`, `/posts`, `/offers`, `/routes` a los servicios de dominio. Scores se consume internamente mediante `http://scores-app-service`, sin ruta pública en el Ingress. Para que el admission webhook de ingress-nginx funcione, el SG de los nodos debe permitir al control plane el puerto 8443 (ver `terraform/modules/eks/main.tf`).

## Pruebas

Pruebas unitarias con Pytest. Las llamadas salientes se simulan con `respx`
(adaptadores) o con puertos mockeados (`AsyncMock`, casos de uso y routers).

- **Casos de uso:** camino feliz, cada validación de RF-004, propagación de
  errores downstream, compensación al fallar el score y fallo de la compensación.
- **Routers:** envoltura 201, mapeo 400/401/403/404/412/503, reenvío del token.
- **Adaptadores:** proyección de respuestas, mapeo de códigos a errores del
  dominio, reintento en GET y ausencia de reintento en POST.

```bash
make unittest DIR=orchestrator_app
make lintcheck DIR=orchestrator_app
```

## Decisiones de diseño

- **Orquestación, no coreografía.** La Entrega 2 no dispone de infraestructura
  asíncrona (colas/eventos); el flujo es una saga síncrona con compensación,
  concentrada en un único componente sin estado. Ver
  `docs/_build/adr/0001-orchestrator-for-composite-requirements.md`.
- **El Ingress es el punto de entrada único.** El orquestador solo atiende
  `/rf00x`; enrutar el tráfico de paso por un proceso Python añadiría un salto y
  un cuello de botella de escalabilidad.
- **El orquestador no calcula la utilidad.** La fórmula y su persistencia son de
  `scores_app`; aquí solo se envían las entradas. Mantiene la regla en un único
  lugar y evita duplicar funcionalidad.
- **Reintentos solo en GET.** Reintentar un POST podría duplicar escrituras y
  romper la consistencia exigida por RF-004.
- **Consistencia estricta oferta + score.** El 201 de RF-004 afirma que la
  utilidad queda almacenada; el `null` de RF-005 es para indisponibilidad de
  lectura, no para una oferta permanentemente sin score. Por eso, si el paso de
  score falla, la oferta se elimina (compensación) antes de responder 503.
- **Puerto de score.** `ScorePort` desacopla el caso de uso de la implementación
  concreta; `HttpScoreAdapter` llama a `scores_app` sin tocar código de casos de uso.
