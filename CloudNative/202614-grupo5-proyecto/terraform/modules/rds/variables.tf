variable "db_name" {
  description = "Nombre de la base de datos única que aloja todas las tablas desacopladas."
  type        = string
}

variable "db_username" {
  description = "Usuario administrador de la base de datos."
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Contraseña del usuario administrador (8-128 chars, sin '/', '\"' ni '@')."
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
  description = "Indica si la instancia es accesible públicamente."
  type        = bool
  default     = false
}

variable "sg_ingress_cidr_blocks" {
  description = "CIDRs permitidos hacia el puerto 5432. Vacío = CIDR de la VPC por defecto."
  type        = list(string)
  default     = []
}
