# Stack `database`

Provisiona la **base de datos única** y publica sus datos de
conexión en Secrets Manager. Se aplica antes que el stack `apps`.

## Componentes

| Componente | Módulo | Responsabilidad |
|---|---|---|
| RDS PostgreSQL | [`modules/rds`](../../modules/rds) | Instancia única `postgres 16` `db.t3.micro` sobre la VPC por defecto, subnet group en todas las subredes, SG que abre 5432 al CIDR de la VPC. Base `clonatdevs` con todas las tablas desacopladas |
| Secrets Manager | [`modules/secrets_manager`](../../modules/secrets_manager) | Secreto JSON con host/puerto/usuario/clave/db (informativo; los pods reciben las credenciales por `envsubst` del pipeline) |

## Entradas (`terraform/environments/<env>/database/terraform.tfvars`)

| Variable | Default | Notas |
|---|---|---|
| `aws_region` | `us-east-1` | Fija por reglas del curso |
| `owner` | — | Usuario dueño (tag) |
| `db_name` | `clonatdevs` | Base única |
| `db_engine_version` | `16` | |
| `db_instance_class` | `db.t3.micro` | |
| `db_allocated_storage_gib` | `20` | |
| `db_publicly_accessible` | `false` | |
| `sg_ingress_cidr_blocks` | `[]` | Vacío = CIDR de la VPC por defecto |
| `secret_name` | `clonatdevs/db` | Prefijo del secreto |
| `db_username` / `db_password` | — | `-var` del pipeline (secrets `DB_USERNAME`/`DB_PASSWORD`) o `secret.auto.tfvars` local |

## Salidas

`db_host`, `db_port`, `db_name`, `db_secret_arn`. El pipeline las expone como
`${DB_HOST}` … para el `envsubst` de los manifiestos en `k8s/aws/`.

## Uso

```bash
make bootstrap-state ENV=student1                 # una vez por cuenta
make tf-init  ENV=student1 STACK=database
make tf-plan  ENV=student1 STACK=database
make tf-apply ENV=student1 STACK=database
```

Credenciales locales: crear `terraform/environments/<env>/database/secret.auto.tfvars` (gitignored):

```hcl
db_username = "clonatdevs"
db_password = "mi-clave-de-prueba"
```
