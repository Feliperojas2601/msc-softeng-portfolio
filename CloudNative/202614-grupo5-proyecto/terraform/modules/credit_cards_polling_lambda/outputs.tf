output "lambda_arn" {
  value       = var.lambda_enabled ? aws_lambda_function.polling[0].arn : null
  description = "ARN de la Lambda cuando está habilitada."
}

output "queue_url" {
  value       = local.queue_url
  description = "URL de la cola de polling."
}

output "queue_arn" {
  value       = local.queue_arn
  description = "ARN de la cola de polling."
}

output "dead_letter_queue_arn" {
  value       = var.create_queue ? aws_sqs_queue.dead_letter[0].arn : null
  description = "ARN de la DLQ cuando este módulo crea la cola."
}
