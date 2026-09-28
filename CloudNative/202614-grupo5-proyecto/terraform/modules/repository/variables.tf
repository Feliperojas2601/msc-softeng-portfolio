variable "repository_name" {
  description = "Nombre del repositorio ECR."
  type        = string
  nullable    = false
}

variable "keep_tags_number" {
  description = "Cantidad de imágenes a conservar en el repositorio."
  type        = number
  default     = 5
}
