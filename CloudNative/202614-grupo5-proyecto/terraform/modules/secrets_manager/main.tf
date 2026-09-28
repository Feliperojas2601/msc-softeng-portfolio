# Sufijo aleatorio para evitar colisiones con secretos en periodo de borrado.
resource "random_id" "suffix" {
  byte_length = 4

  keepers = {
    name_prefix = var.secret_name
  }
}

# Datos de conexión de la base de datos. Informativo: los pods reciben las
# credenciales por envsubst del pipeline, no leen este secreto.
resource "aws_secretsmanager_secret" "this" {
  name        = "${var.secret_name}-${random_id.suffix.hex}"
  description = "Credenciales y datos de conexión de la base de datos RDS."
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id = aws_secretsmanager_secret.this.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    engine   = var.db_engine
    host     = var.db_host
    port     = var.db_port
    dbname   = var.db_name
  })
}
