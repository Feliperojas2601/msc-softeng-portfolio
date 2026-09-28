variable "aws_region" {
  description = "Región de AWS. Fija en us-east-1 por reglas del curso."
  type        = string
  default     = "us-east-1"
}

variable "owner" {
  description = "Usuario dueño de los recursos (para tags). Fines académicos."
  type        = string
}

variable "cluster_name" {
  description = "Nombre del clúster EKS. Debe aparecer como línea literal `cluster_name = \"...\"` en terraform.tfvars: el pipeline la lee con grep."
  type        = string
  default     = "clonatdevs-eks"
}

variable "k8s_cluster_version" {
  description = "Versión de Kubernetes del clúster EKS."
  type        = string
  default     = "1.33"
}

variable "cluster_endpoint_public_access" {
  description = "Habilita el acceso público al endpoint del clúster."
  type        = bool
  default     = true
}

variable "node_instance_types" {
  description = "Tipos de instancia del node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Cantidad deseada de nodos worker."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Cantidad mínima de nodos worker."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Cantidad máxima de nodos worker."
  type        = number
  default     = 3
}

variable "keep_tags_number" {
  description = "Cantidad de imágenes a conservar por repositorio ECR."
  type        = number
  default     = 5
}

# NO configurar esto como secret de GitHub: GitHub Actions detecta cuando un
# output de job (tf_outputs) contiene un valor igual a un secret registrado
# y descarta el output COMPLETO ("Skip output 'tf_outputs' since it may
# contain secret"), lo que rompe también ecr_registry, db_host, db_port,
# etc. para TODAS las apps (no solo TrueNative). No es un credential real:
# es un token que el equipo define libremente para autenticar las llamadas
# entre nuestros componentes y TrueNative ("cualquier cadena de caracteres
# definida por usted", según la documentación de TrueNative). Se define
# como variable normal, con el mismo valor en terraform.tfvars de cada
# ambiente.
variable "true_native_secret_token" {
  description = "SECRET_TOKEN compartido con TrueNative (no es un credential externo, ver comentario arriba)."
  type        = string
  sensitive   = true
}

# El pipeline pasa db_username / db_password como -var a TODOS los stacks.
# Este stack no las usa; se declaran solo para evitar el warning de variable
# no declarada.
variable "db_username" {
  description = "No se usa en este stack (requerida por el pipeline)."
  type        = string
  default     = ""
  sensitive   = true
}

variable "db_password" {
  description = "No se usa en este stack (requerida por el pipeline)."
  type        = string
  default     = ""
  sensitive   = true
}

# La Lambda de polling (y sus variables de configuración: URLs, role,
# etc.) vive en el stack credit-cards-polling-lambda (post_k8s_stacks), no
# aquí. Este stack solo crea la cola SQS que la alimenta.
variable "credit_cards_internal_secret" {
  description = "Token compartido entre la Lambda y el endpoint interno de tarjetas."
  type        = string
  default     = "change-me-internal"
}
