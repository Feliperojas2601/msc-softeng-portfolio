locals {
  ecr_repositories = [
    "users_app",
    "posts_app",
    "offers_app",
    "routes_app",
    "orchestrator_app",
    "scores_app",
    "identity_webhook_app",
    "notifications_app",
    "credit_cards_app",
    "credit_cards_mediator_app",
  ]

  # Ver data.tf: EMAIL_TO_NOTIFY viene de Secrets Manager, no de una variable.
  pipeline_native_map = jsondecode(data.aws_secretsmanager_secret_version.pipeline_native_map.secret_string)
  email_to_notify     = local.pipeline_native_map["EMAIL_TO_NOTIFY"]
}
