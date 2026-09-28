output "secret_arn" {
  description = "ARN del secreto en AWS Secrets Manager."
  value       = aws_secretsmanager_secret.this.arn
}

output "secret_name" {
  description = "Nombre final del secreto (con sufijo)."
  value       = aws_secretsmanager_secret.this.name
}
