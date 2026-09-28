locals {
  # Si no se pasan CIDRs, se permite solo el rango de la VPC por defecto
  # (donde viven los nodos del clúster).
  ingress_cidr_blocks = length(var.sg_ingress_cidr_blocks) > 0 ? var.sg_ingress_cidr_blocks : [data.aws_vpc.default.cidr_block]
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.db_name}-subnet-group"
  subnet_ids = data.aws_subnets.all.ids
}

resource "aws_security_group" "this" {
  name        = "${var.db_name}-rds-sg"
  description = "Acceso a PostgreSQL desde la VPC"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = local.ingress_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Instancia única de PostgreSQL: todos los servicios comparten esta base y
# cada uno gestiona sus propias tablas (sin llaves foráneas entre servicios).
resource "aws_db_instance" "this" {
  identifier     = "${var.db_name}-postgres"
  engine         = "postgres"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  allocated_storage = var.db_allocated_storage_gib
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.this.id]
  publicly_accessible    = var.db_publicly_accessible
  multi_az               = false

  skip_final_snapshot     = true
  deletion_protection     = false
  backup_retention_period = 0
  apply_immediately       = true
}
