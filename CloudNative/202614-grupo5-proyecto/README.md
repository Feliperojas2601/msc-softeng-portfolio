# proyecto-base

Plataforma de logística de encomiendas entre viajeros (estilo "encarga algo"),
compuesta por seis aplicaciones Python/FastAPI con arquitectura hexagonal:
`users_app`, `posts_app`, `offers_app`, `routes_app`, `scores_app` y
`orchestrator_app`. En la Entrega 2 se despliegan en AWS EKS mediante Terraform
y comparten una base PostgreSQL en RDS llamada `clonatdevs`, con propiedad
exclusiva de tablas por microservicio. El orquestador consume las APIs internas
sin acceder a RDS. El Ingress centraliza las rutas públicas; Scores es interno.

## Tabla de contenido

- [proyecto-base](#proyecto-base)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Archivo de configuración](#archivo-de-configuración)
  - [Aplicaciones](#aplicaciones)
  - [Despliegue evaluado en AWS (Entrega 2)](#despliegue-evaluado-en-aws-entrega-2)
  - [Notificaciones por correo (Entrega 3)](#notificaciones-por-correo-entrega-3)
    - [Arquitectura](#arquitectura)
    - [Configuración](#configuración)
    - [Paso manual obligatorio: confirmar la suscripción de correo](#paso-manual-obligatorio-confirmar-la-suscripción-de-correo)
    - [Correo temporal para el ambiente `tutor`](#correo-temporal-para-el-ambiente-tutor)
  - [Requisitos previos](#requisitos-previos)
  - [Despliegue local con Docker Compose](#despliegue-local-con-docker-compose)
  - [Despliegue de todos los componentes en Minikube](#despliegue-de-todos-los-componentes-en-minikube)
    - [1. Iniciar el clúster](#1-iniciar-el-clúster)
    - [2. Construir y cargar las imágenes](#2-construir-y-cargar-las-imágenes)
    - [3. Desplegar los manifiestos](#3-desplegar-los-manifiestos)
    - [4. Verificar el despliegue](#4-verificar-el-despliegue)
    - [5. Acceder a cada servicio](#5-acceder-a-cada-servicio)
    - [6. Detener y limpiar](#6-detener-y-limpiar)
  - [Pruebas](#pruebas)
  - [Documentación](#documentación)
  - [Arquitectura RF-006 y preparación de despliegue](#arquitectura-rf-006-y-preparación-de-despliegue)

## Estructura del Proyecto

```
.
├── .github/
│   └── workflows/           # Pipelines del repositorio (CI de unit tests, k8s y docs)
├── docs/                    # Documentación técnica (vistas de arquitectura y diagramas)
│   ├── diagrams/            # Diagramas PlantUML (componentes, despliegue, entidades, redes)
│   └── README.md            # Página raíz de la documentación (GitHub Pages)
├── k8s/                     # Manifiestos de despliegue en Kubernetes, uno por aplicación
│   ├── users_app.yaml
│   ├── posts_app.yaml
│   ├── offers_app.yaml
│   ├── routes_app.yaml
│   ├── scores_app.yaml       # Manifiesto local
│   └── aws/                  # Manifiestos EKS de las seis apps y el Ingress
├── users_app/               # API de usuarios: registro, autenticación y perfiles
├── posts_app/               # API de publicaciones (viajes con espacio disponible)
├── offers_app/              # API de ofertas sobre una publicación
├── routes_app/              # API de trayectos (origen, destino y fechas de un vuelo)
├── scores_app/              # Cálculo y persistencia de utilidad
├── orchestrator_app/        # Composición de RF-003, RF-004 y RF-005
├── terraform/               # Infraestructura AWS
│   ├── modules/             # Módulos reutilizables: EKS, RDS, ECR y secretos
│   ├── stacks/              # Unidades desplegables: database y apps
│   └── environments/        # Configuración student1, student2, student3 y student4
├── pets_app/                # Proyecto de ejemplo de referencia (no forma parte del despliegue)
├── config.yaml              # Configuración del equipo y de la evaluación automática
├── makefile                 # Scripts comunes de lint y pruebas unitarias por aplicación
└── README.md                # Este archivo
```

1. **`.github/workflows`**: los archivos en esta carpeta no se pueden modificar a excepción de `ci_evaluador_unit.yml`, que debe tener un job por aplicación.
2. **`k8s`**: los archivos `*.yaml` de esta carpeta corresponden al entorno local, con PostgreSQL en contenedores. `k8s/aws/` contiene los manifiestos evaluados en EKS; las bases de datos no se despliegan como pods, ya que la persistencia está en RDS.
3. **`docs`**: documentación técnica publicada en GitHub Pages, con las vistas de información, funcional, de despliegue y de desarrollo, más sus diagramas en `diagrams/`.
4. **`<aplicación>`**: una carpeta por cada API. Todas siguen la misma estructura interna (`src/domain`, `src/adapters`, `src/entrypoints`, `tests/`); consulte el `README.md` de cada una para el detalle de endpoints y modelos.
5. **`makefile`**: utilizado por los pipelines evaluadores y por los desarrolladores para correr lint y pruebas unitarias de una aplicación puntual (`make unittest DIR=<aplicación>`).

## Archivo de configuración

El archivo `config.yaml` contiene la información del equipo, el enlace al tablero y a la documentación, y el nombre/tag de imagen de cada aplicación. Debe mantenerse sincronizado con los nombres usados en `k8s/` y en cada `Dockerfile`; si no está correctamente configurado la entrega no puede evaluarse.

`tf_stacks` define el orden `database` → `apps`; `post_k8s_stacks` agrega `credit_cards_polling`, aplicado despues de `k8s_manifests` (necesita los balanceadores internos que ese paso crea). `default_env` selecciona `student1` como base para el ambiente del tutor. `k8s_manifests` selecciona `k8s/aws` y `apps` declara las seis imágenes a construir y publicar.

## Aplicaciones

| Aplicación | Puerto en AWS | Persistencia en AWS | README |
|---|---|---|---|
| `users_app` | `30000` | Tablas propias en `clonatdevs` | [Usuarios](./users_app/README.md) |
| `posts_app` | `30001` | Tablas propias en `clonatdevs` | [Publicaciones](./posts_app/README.md) |
| `routes_app` | `30002` | Tablas propias en `clonatdevs` | [Trayectos](./routes_app/README.md) |
| `offers_app` | `30003` | Tablas propias en `clonatdevs` | [Ofertas](./offers_app/README.md) |
| `scores_app` | `30004` | Tablas propias en `clonatdevs` | [Scores](./scores_app/README.md) |
| `orchestrator_app` | `30005` | Sin base de datos | [Orquestador](./orchestrator_app/README.md) |

Los Services reciben tráfico interno por el puerto `80`. Scores y Orchestrator son `ClusterIP`; los otros cuatro conservan `NodePort`. El acceso público previsto utiliza el host del Ingress.

`pets_app` es el proyecto de ejemplo entregado como guía de arquitectura hexagonal ([pets_app/README.md](./pets_app/README.md)); no tiene `Dockerfile` ni manifiesto de `k8s` propio y no participa del despliegue de la plataforma.

## Despliegue evaluado en AWS (Entrega 2)

Con las credenciales del ambiente configuradas en GitHub Actions y `config.yaml` actualizado, ejecutar sobre el mismo ambiente:

1. `ci_entrega2_deploy.yml`: despliega los stacks `database` y `apps`, publica las imágenes en ECR y aplica `k8s/aws/`.
2. `ci_entrega2_evaluador.yml`: valida los requerimientos sobre el despliegue anterior.
3. `ci_entrega2_destroy.yml`: elimina la infraestructura después de terminar la evaluación.

El Ingress publica `/users`, `/posts`, `/offers`, `/routes` y los prefijos `/rf003`, `/rf004`, `/rf005`. El orquestador llama a Scores mediante `http://scores-app-service`; no existe una ruta pública `/scores`.

La configuración por ambiente se encuentra en `terraform/environments/`. Consulte los README de [database](./terraform/stacks/database/README.md) y [apps](./terraform/stacks/apps/README.md).

## Notificaciones por correo (Entrega 3)

Los resultados de la verificación de identidad (RF-007) y, de tarjetas de crédito (RF-006) se notifican al usuario por correo electrónico usando **Amazon SNS**.

### Arquitectura

- `identity_webhook_app` publica el resultado de identidad y el Mediator de tarjetas publicará el resultado de verificación llamando a `notifications_app` mediante `POST /notify` — comunicación HTTP síncrona, interna al clúster, sin exponer ruta pública. `credit_cards_app` solo realiza la creación inicial y no bloquea el POST esperando correo.
- `notifications_app` es el **único** componente del sistema que interactúa con AWS SNS: recibe el evento, construye el contenido del correo y publica el mensaje (`sns:Publish`) a un Topic de SNS creado por Terraform.
- El Topic tiene una suscripción de tipo `email` hacia la dirección definida en el secret `EMAIL_TO_NOTIFY`. SNS entrega el correo directamente al suscriptor; no se usa ningún servicio adicional de envío (SES, SMTP, etc.).

Esta decisión evita que `users_app`, `identity_webhook_app` o `credit_cards_app` necesiten credenciales de AWS. Solo `notifications_app` requiere el permiso `sns:Publish`, usando las mismas credenciales de sesión temporales que ya usa el pipeline para Terraform (inyectadas como variable de entorno al Pod). No se crea ningún rol ni política de IAM nuevos — la cuenta de AWS Academy (Learner Lab) no lo permite, solo reutiliza roles ya existentes.

### Configuración

| Elemento | Dónde se configura |
|---|---|
| `EMAIL_TO_NOTIFY` | Secret de GitHub Actions (`Settings → Secrets and variables → Actions`). Obligatorio, independiente del servicio de notificación elegido. |
| Disponibilidad para Terraform | El pipeline del curso replica automáticamente el valor de `EMAIL_TO_NOTIFY` en AWS Secrets Manager, dentro de `secrets-pipeline-native-map`. El Terraform de notificaciones lee el correo desde ahí para crear la suscripción del Topic. |
| Topic y suscripción de SNS | Se crean por Terraform al desplegar el stack de notificaciones. |

### Paso manual obligatorio: confirmar la suscripción de correo

AWS SNS exige confirmar manualmente cada suscripción de tipo `email` antes de empezar a entregar mensajes — es una medida de seguridad de AWS, no configurable desde Terraform.

Cada vez que se despliega el stack de notificaciones desde cero (Topic nuevo):

1. Se ejecuta `ci_entrega2_deploy.yml`.
2. Terraform crea el Topic de SNS y la suscripción de email hacia `EMAIL_TO_NOTIFY`.
3. AWS envía automáticamente un correo a esa dirección, remitente `AWS Notifications <no-reply@sns.amazonaws.com>`, asunto **"AWS Notification - Subscription Confirmation"**.
4. **Es necesario abrir ese correo y hacer clic en "Confirm subscription"** antes de continuar. Si no se confirma, SNS nunca entrega los correos de resultado de verificación, aunque el resto del sistema funcione correctamente.
5. Solo después de confirmar la suscripción se debe ejecutar `ci_evaluador_entrega3.yml`, para que las pruebas de notificación por correo puedan pasar.
6. Al finalizar, ejecutar `ci_entrega2_destroy.yml` para eliminar la infraestructura, incluidos el Topic y su suscripción.

Orden completo: `deploy` → confirmar suscripción de SNS manualmente → `evaluador` → `destroy`.

### Correo temporal para el ambiente `tutor`

Para poder ver de verdad los correos que SNS entrega cuando se corre el pipeline contra el ambiente `tutor` (el único que cuenta para la calificación), hay que usar una dirección a la que se tenga acceso en el momento del despliegue:

1. Antes de correr `ci_entrega2_deploy.yml`, entrar a [temp-mail.org](https://temp-mail.org/es/) y generar una dirección de correo temporal. **No cerrar ni refrescar esa pestaña** hasta terminar el paso 4.
2. Actualizar el secret `EMAIL_TO_NOTIFY` del **environment `tutor`** en GitHub (`Settings → Environments → tutor → Secrets`) con esa dirección temporal.
3. Ejecutar `ci_entrega2_deploy.yml` para el ambiente `tutor`. Terraform crea el Topic de SNS y la suscripción hacia esa dirección temporal.
4. Revisar la bandeja de [temp-mail.org](https://temp-mail.org/es/) (la misma pestaña abierta en el paso 1) por el correo de confirmación de AWS y hacer clic en **"Confirm subscription"**.
5. Solo después de confirmar, ejecutar el pipeline evaluador (`ci_entrega3_evaluador.yml` o `ci_entrega3_email_evaluador.yml`). Los correos de resultado (RF-006/RF-007) van a llegar a esa misma bandeja temporal, donde se pueden observar en tiempo real.

Si la pestaña del correo temporal se cierra o se refresca antes de confirmar, la dirección se pierde junto con la suscripción pendiente — hay que repetir desde el paso 1 con una dirección nueva.

## Requisitos previos

- Python 3.11+ y [Poetry](https://python-poetry.org/) 2.1.1
- Docker y Docker Compose
- [Minikube](https://minikube.sigs.k8s.io/) y `kubectl`
- Postman (para las colecciones de pruebas de integración de cada aplicación)

## Despliegue local con Docker Compose

Para levantar una aplicación individual junto con su propia base de datos, ejecute desde la carpeta de esa aplicación:

```bash
cd <aplicación>       # p. ej. users_app, posts_app, routes_app u offers_app
docker compose up --build
```

Esto crea la app y su Postgres en una red aislada de Docker Compose, usando los puertos indicados en la tabla de [Aplicaciones](#aplicaciones). Repita el comando en otra terminal por cada aplicación que necesite levantar en paralelo. Para el detalle de variables de entorno, endpoints y ejecución sin Docker, revise el `README.md` de cada aplicación.

## Despliegue de todos los componentes en Minikube

Esta sección despliega las cuatro aplicaciones y sus bases de datos en un mismo clúster de Minikube, como referencia del entorno local de la Entrega 1. La evaluación de la Entrega 2 utiliza el despliegue AWS descrito arriba.

### 1. Iniciar el clúster

Los manifiestos usan `NetworkPolicy` para aislar cada base de datos, por lo que el clúster debe iniciarse con un CNI que las soporte (el CNI por defecto de Minikube, `kindnet`, las ignora):

```bash
minikube start --cpus=4 --memory=6g --cni calico
```

### 2. Construir y cargar las imágenes

Construya la imagen de cada aplicación con el tag definido en `config.yaml` (`v1.0.0`) y cárguela directamente en el clúster de Minikube:

```bash
for app in users_app posts_app routes_app offers_app; do
  docker build --rm --platform linux/amd64 \
    -t ${app}:v1.0.0 \
    -f ${app}/Dockerfile \
    --target runner \
    ${app}

  minikube image load ${app}:v1.0.0
done
```

### 3. Desplegar los manifiestos

Aplique los manifiestos de las cuatro aplicaciones construidas en el paso anterior:

```bash
kubectl apply -f k8s/users_app.yaml -f k8s/posts_app.yaml -f k8s/routes_app.yaml -f k8s/offers_app.yaml
```

Cada manifiesto crea, para su aplicación: el `Secret` con las credenciales de la base de datos, el `Deployment`/`Service` de Postgres, el `Deployment`/`Service` de la API (con un `initContainer` que espera a que la base de datos esté lista) y la `NetworkPolicy` que solo permite tráfico hacia la base de datos desde su propia app.

### 4. Verificar el despliegue

```bash
kubectl wait --for=condition=ready pod -l app=users-app  --timeout=180s
kubectl wait --for=condition=ready pod -l app=posts-app  --timeout=180s
kubectl wait --for=condition=ready pod -l app=routes-app --timeout=180s
kubectl wait --for=condition=ready pod -l app=offers-app --timeout=180s

kubectl get pods,svc
```

### 5. Acceder a cada servicio

```bash
minikube service users-app-service  --url
minikube service posts-app-service  --url
minikube service routes-app-service --url
minikube service offers-app-service --url
```

Cada comando imprime la URL asignada por Minikube; use esa URL como `baseUrl` en la colección de Postman correspondiente (`tests/api/*.postman_collection.json` de cada aplicación) o consúltela directamente en `http://<url>/docs` para la documentación Swagger.

Para confirmar que el aislamiento de red funciona (debe responder `BLOCKED`), revise la sección "Verificar NetworkPolicy" del `README.md` de cada aplicación.

### 6. Detener y limpiar

```bash
kubectl delete -f k8s/users_app.yaml -f k8s/posts_app.yaml -f k8s/routes_app.yaml -f k8s/offers_app.yaml
minikube stop        # o `minikube delete` para eliminar el clúster por completo
```

## Pruebas

Cada aplicación incluye pruebas unitarias (Pytest) y una colección de Postman para pruebas de integración. Desde la raíz del repositorio puede ejecutar lint y pruebas unitarias de una aplicación puntual con:

```bash
make unittest DIR=<aplicación>
make lintcheck DIR=<aplicación>
```

Consulte la sección "Pruebas" del `README.md` de cada aplicación para el detalle de cobertura mínima y ejecución de la colección de Postman con Newman.

## Documentación

La documentación técnica completa (vistas de información, funcional, de despliegue y de desarrollo, con sus diagramas) está en [docs/README.md](./docs/README.md) y publicada en GitHub Pages según el enlace `docs` de `config.yaml` y a continuacion:

https://silver-couscous-pzo5v4j.pages.github.io/

## Arquitectura RF-006 y preparación de despliegue

El diseño de creación de tarjetas usa Mediator para coordinar polling de TrueNative y correo fuera de la petición HTTP inicial. Consulte el [proceso RF-006](./docs/requerimientos/rf-006.md), la [vista de componentes](./docs/requerimientos/rf-006.md#vista-funcional-y-componentes), los [patrones](./docs/patrones-solucion.md#rf-006---crear-tarjetas-de-crédito) y el [despliegue propuesto](./docs/requerimientos/rf-006.md#vista-de-despliegue-y-operación).

La carpeta `credit_cards_app/` implementa el listado autenticado, los endpoints count/ping/reset, la creación síncrona con TrueNative y el endpoint interno idempotente para finalizar la verificación. Su [README](./credit_cards_app/README.md) describe el contrato, configuración y pruebas. `notifications_app/` ya publica resultados en SNS. `credit_cards_mediator_app/` implementa el worker de polling en contenedor (sin Lambda ni SQS) para consultar TrueNative y actualizar el estado. El documento está en `docs/requerimientos/rf-006.md`; el modelo de secuencia y su imagen PlantUML en `docs/diagrams/rf006-sequence.*`.

Antes de desplegar RF-006, aprovisionar la base exclusiva y SNS. `credit_cards_app`, `notifications_app` y `credit_cards_mediator_app` se despliegan los tres como imágenes de contenedor mediante `k8s/aws/`, igual que el resto de las apps — no hay Lambda ni SQS que aprovisionar ni ningún stack adicional en `post_k8s_stacks`. La configuración actual mantiene los stacks `database` y `apps`, el ambiente `student1` y `k8s/aws`. Las condiciones y la estructura requerida se detallan en [configuración declarativa](./docs/requerimientos/rf-006.md#configuración-declarativa).

Desplegar en `us-east-1`, con recursos de aplicación en `default` y LabRole existente, verificando permisos sin crear roles IAM. Mantener intactos los workflows protegidos. Configurar `EMAIL_TO_NOTIFY` en GitHub y en el secreto AWS `secrets-pipeline-native-map`. Tras `ci_entrega2_deploy.yml`, **confirmar manualmente la suscripción SNS por correo antes de evaluar** con `ci_entrega3_evaluador.yml` o su variante de email. Finalizada la evaluación, utilizar `ci_entrega2_destroy.yml` según las reglas del entorno.

Este cambio documenta la arquitectura: no despliega RF-006 ni publica el sitio remoto. La navegación local queda incorporada al índice existente de `docs/README.md`; integrar y publicar por el mecanismo de GitHub Pages configurado es un paso posterior.
