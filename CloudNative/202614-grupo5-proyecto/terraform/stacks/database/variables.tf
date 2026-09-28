variable "aws_region" {
  description = "Región de AWS. Fija en us-east-1 por reglas del curso."
  type        = string
  default     = "us-east-1"
}

variable "owner" {
  description = "Usuario dueño de los recursos (para tags). Fines académicos."
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos única."
  type        = string
  default     = "clonatdevs"
}

variable "db_username" {
  description = "Usuario administrador de la BD. Lo pasa el pipeline como -var (secret DB_USERNAME) o localmente en secret.auto.tfvars."
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Contraseña del administrador de la BD (8-128 chars, sin '/', '\"' ni '@')."
  type        = string
  sensitive   = true
}

variable "db_engine_version" {
  description = "Versión de PostgreSQL."
  type        = string
  default     = "16"
}

variable "db_instance_class" {
  description = "Clase de instancia RDS."
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage_gib" {
  description = "Almacenamiento asignado en GiB."
  type        = number
  default     = 20
}

variable "db_publicly_accessible" {
  description = "Indica si la BD es accesible públicamente."
  type        = bool
  default     = false
}

variable "sg_ingress_cidr_blocks" {
  description = "CIDRs permitidos hacia el puerto 5432. Vacío = CIDR de la VPC por defecto."
  type        = list(string)
  default     = []
}

variable "secret_name" {
  description = "Prefijo del secreto de conexión en AWS Secrets Manager."
  type        = string
  default     = "clonatdevs/db"
}
