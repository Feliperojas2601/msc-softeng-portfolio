# Topic de SNS para las notificaciones de resultado (RF-006 y RF-007).
#
# La suscripcion de email entrega el correo directamente -- no se necesita
# SES, SMTP ni codigo de envio propio. AWS exige confirmar manualmente cada
# suscripcion de tipo email antes de que empiece a entregar mensajes; ver
# el README de la raiz del repo ("Notificaciones por correo") para el paso
# manual completo.
resource "aws_sns_topic" "this" {
  name = var.topic_name
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.this.arn
  protocol  = "email"
  endpoint  = var.email_subscription
}
