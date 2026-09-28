variable "name" {
  type        = string
  description = "Nombre base de las colas de verificación."
}

variable "visibility_timeout_seconds" {
  type        = number
  description = "Tiempo de visibilidad superior al timeout de la Lambda que la consume."
  default     = 180
}

variable "message_retention_seconds" {
  type        = number
  description = "Retención de mensajes en las colas."
  default     = 1209600
}

variable "max_receive_count" {
  type        = number
  description = "Intentos antes de mover un mensaje a la DLQ."
  default     = 5
}
