output "address" {
  description = "Endpoint (host) de la instancia RDS."
  value       = aws_db_instance.this.address
}

output "port" {
  description = "Puerto de la instancia RDS."
  value       = aws_db_instance.this.port
}

output "engine" {
  description = "Motor de la base de datos."
  value       = aws_db_instance.this.engine
}

output "db_name" {
  description = "Nombre de la base de datos."
  value       = aws_db_instance.this.db_name
}
