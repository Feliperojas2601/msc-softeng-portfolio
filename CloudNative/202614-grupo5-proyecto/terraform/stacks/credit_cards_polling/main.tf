locals {
  lambda_connectivity_service_names = {
    notifications = "notifications-lambda-service"
    users         = "users-app-lambda-service"
    credit_cards  = "credit-cards-app-lambda-service"
    true_native   = "true-native-lambda-service"
  }

  lambda_connectivity_hostnames = {
    for key, svc in data.kubernetes_service_v1.lambda_connectivity :
    key => try(svc.status[0].load_balancer[0].ingress[0].hostname, "")
  }

  # Resueltos automaticamente, salvo que el ambiente los sobreescriba en
  # terraform.tfvars.
  lab_role_arn = tolist(data.aws_iam_roles.lab_role.arns)[0]
  lambda_role_arn = (
    var.lambda_role_arn != "" ? var.lambda_role_arn : local.lab_role_arn
  )
  subnet_ids = (
    length(var.subnet_ids) > 0 ? var.subnet_ids : data.aws_subnets.all.ids
  )
  security_group_ids = (
    length(var.security_group_ids) > 0 ?
    var.security_group_ids : [aws_security_group.lambda.id]
  )

  notifications_api_base_url = (
    var.notifications_api_base_url != "" ? var.notifications_api_base_url :
    (lookup(local.lambda_connectivity_hostnames, "notifications", "") != "" ?
    "http://${local.lambda_connectivity_hostnames["notifications"]}" : "")
  )
  users_api_base_url = (
    var.users_api_base_url != "" ? var.users_api_base_url :
    (lookup(local.lambda_connectivity_hostnames, "users", "") != "" ?
    "http://${local.lambda_connectivity_hostnames["users"]}" : "")
  )
  cards_api_base_url = (
    var.cards_api_base_url != "" ? var.cards_api_base_url :
    (lookup(local.lambda_connectivity_hostnames, "credit_cards", "") != "" ?
    "http://${local.lambda_connectivity_hostnames["credit_cards"]}" : "")
  )
  true_native_base_url = (
    var.true_native_base_url != "" ? var.true_native_base_url :
    (lookup(local.lambda_connectivity_hostnames, "true_native", "") != "" ?
    "http://${local.lambda_connectivity_hostnames["true_native"]}" : "")
  )
}

# Security group propio de la Lambda: solo egreso, para alcanzar SQS (via
# NAT/endpoint de la VPC default) y los balanceadores internos. No abre
# ingreso porque Lambda no recibe conexiones entrantes.
resource "aws_security_group" "lambda" {
  name        = "clonatdevs-credit-cards-polling-lambda"
  description = "Egreso de la Lambda de polling de tarjetas hacia SQS y servicios internos."
  vpc_id      = data.aws_vpc.default.id

  egress {
    description = "Salida HTTP/HTTPS y SQS"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "credit_cards_polling_lambda" {
  source = "../../modules/credit_cards_polling_lambda"

  lambda_enabled                   = var.lambda_enabled
  lambda_role_arn                  = local.lambda_role_arn
  lambda_source_dir                = "${path.root}/../../../credit_cards_mediator_app/src"
  subnet_ids                       = local.subnet_ids
  security_group_ids               = local.security_group_ids
  queue_url                        = data.aws_sqs_queue.polling.url
  queue_arn                        = data.aws_sqs_queue.polling.arn
  queue_visibility_timeout_seconds = var.queue_visibility_timeout_seconds
  true_native_base_url             = local.true_native_base_url
  true_native_secret_token         = var.true_native_secret_token
  cards_api_base_url               = local.cards_api_base_url
  cards_api_secret                 = var.cards_api_secret != "" ? var.cards_api_secret : var.credit_cards_internal_secret
  users_api_base_url               = local.users_api_base_url
  notifications_api_base_url       = local.notifications_api_base_url
}
