output "db_host" {
  description = "Endpoint (host) de la base de datos."
  value       = module.rds.address
}

output "db_port" {
  description = "Puerto de la base de datos."
  value       = tostring(module.rds.port)
}

output "db_name" {
  description = "Nombre de la base de datos."
  value       = module.rds.db_name
}

output "db_secret_arn" {
  description = "ARN del secreto de conexión en AWS Secrets Manager."
  value       = module.secrets_manager.secret_arn
}
