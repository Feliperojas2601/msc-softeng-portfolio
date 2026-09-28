variable "topic_name" {
  description = "Nombre del Topic de SNS."
  type        = string
}

variable "email_subscription" {
  description = "Correo suscrito al Topic (EMAIL_TO_NOTIFY). Requiere confirmacion manual tras el deploy."
  type        = string
}
