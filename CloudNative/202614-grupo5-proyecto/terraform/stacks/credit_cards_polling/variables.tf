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
  description = "Nombre del clúster EKS creado por el stack apps."
  type        = string
  default     = "clonatdevs-eks"
}

variable "lambda_enabled" {
  description = "Activa la Lambda de polling. Default true: este stack corre en post_k8s_stacks, después de que k8s_manifests ya desplegó los balanceadores internos (k8s/aws/credit_cards_polling_connectivity.yml)."
  type        = bool
  default     = true
}

variable "lambda_role_arn" {
  description = "Execution role existente para la Lambda. Vacío = se resuelve automáticamente el ARN de LabRole."
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "Subredes de Lambda. Vacío = se resuelven automáticamente las de la VPC default."
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Security groups de Lambda. Vacío = se crea uno propio de solo egreso."
  type        = list(string)
  default     = []
}

variable "true_native_base_url" {
  description = "URL de TrueNative accesible desde Lambda. Vacío = hostname del balanceador interno leído de k8s."
  type        = string
  default     = ""
}

variable "true_native_secret_token" {
  description = "SECRET_TOKEN compartido con TrueNative (mismo valor que en el stack apps)."
  type        = string
  sensitive   = true
}

variable "cards_api_base_url" {
  description = "URL de credit_cards_app accesible desde Lambda. Vacío = hostname del balanceador interno leído de k8s."
  type        = string
  default     = ""
}

variable "cards_api_secret" {
  description = "Token del endpoint interno de tarjetas. Vacío = usa credit_cards_internal_secret."
  type        = string
  sensitive   = true
  default     = ""
}

variable "credit_cards_internal_secret" {
  description = "Mismo valor que en el stack apps (CREDIT_CARDS_INTERNAL_SECRET)."
  type        = string
  sensitive   = true
  default     = "change-me-internal"
}

variable "users_api_base_url" {
  description = "URL de usuarios accesible desde Lambda. Vacío = hostname del balanceador interno leído de k8s."
  type        = string
  default     = ""
}

variable "notifications_api_base_url" {
  description = "URL de notifications_app accesible desde Lambda, sin /notify. Vacío = hostname del balanceador interno leído de k8s."
  type        = string
  default     = ""
}

variable "queue_visibility_timeout_seconds" {
  description = "Visibilidad de la cola creada en el stack apps (debe coincidir)."
  type        = number
  default     = 180
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
