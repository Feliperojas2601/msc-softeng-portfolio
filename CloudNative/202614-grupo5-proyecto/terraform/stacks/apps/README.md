# Stack `apps`

Provisiona el **clúster EKS** y los **repositorios ECR**. Se
aplica después del stack `database`.

## Componentes

| Componente | Módulo | Responsabilidad |
|---|---|---|
| EKS | [`modules/eks`](../../modules/eks) | Envuelve `terraform-aws-modules/eks/aws ~> 18.31`. Clúster `1.33` sobre la VPC y subredes por defecto, node group gestionado `t3.medium` ×2 (`min 1` / `max 3`). Sin IAM nuevo: usa `LabEksClusterRole` / `LabEksNodeRole` del Learner Lab. Sin IRSA ni gestión de `aws-auth` |
| ECR | [`modules/repository`](../../modules/repository) | Un repositorio por imagen desplegable (6: `users_app`, `posts_app`, `offers_app`, `routes_app`, `orchestrator_app`, `scores_app`), `force_delete = true`, política de ciclo de vida que conserva las últimas N imágenes |

El ingreso (`ingress-nginx`) lo instala el pipeline vía Helm; este stack no lo
gestiona.

## Entradas (`terraform/environments/<env>/apps/terraform.tfvars`)

| Variable | Default | Notas |
|---|---|---|
| `aws_region` | `us-east-1` | Fija por reglas del curso |
| `owner` | — | Usuario dueño (tag) |
| `cluster_name` | `clonatdevs-eks` | **Debe** ser línea literal `cluster_name = "..."` — el pipeline la lee con grep |
| `k8s_cluster_version` | `1.33` | |
| `cluster_endpoint_public_access` | `true` | El pipeline necesita alcanzar el endpoint |
| `node_instance_types` / `node_desired_size` / `node_min_size` / `node_max_size` | `["t3.medium"]` / `2` / `1` / `3` | |
| `keep_tags_number` | `5` | Imágenes a conservar por repo ECR |

## Salidas

`cluster_name`, `cluster_endpoint`, `ecr_registry`, `ecr_repository_urls`.

## Uso

```bash
make tf-init  ENV=student1 STACK=apps
make tf-plan  ENV=student1 STACK=apps
make tf-apply ENV=student1 STACK=apps
```
