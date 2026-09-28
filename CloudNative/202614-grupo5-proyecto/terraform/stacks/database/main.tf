module "rds" {
  source = "../../modules/rds"

  db_name                  = var.db_name
  db_username              = var.db_username
  db_password              = var.db_password
  db_engine_version        = var.db_engine_version
  db_instance_class        = var.db_instance_class
  db_allocated_storage_gib = var.db_allocated_storage_gib
  db_publicly_accessible   = var.db_publicly_accessible
  sg_ingress_cidr_blocks   = var.sg_ingress_cidr_blocks
}

module "secrets_manager" {
  source = "../../modules/secrets_manager"

  secret_name = var.secret_name
  db_username = var.db_username
  db_password = var.db_password
  db_engine   = module.rds.engine
  db_host     = module.rds.address
  db_port     = module.rds.port
  db_name     = module.rds.db_name

  depends_on = [module.rds]
}
