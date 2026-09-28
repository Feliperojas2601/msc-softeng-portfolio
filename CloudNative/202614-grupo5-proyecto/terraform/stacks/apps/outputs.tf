# El pipeline expone cada output como variable de entorno en MAYÚSCULAS.

output "cluster_name" {
  description = "Nombre del clúster EKS (lo usa el pipeline para `aws eks update-kubeconfig`)."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint del API server del clúster."
  value       = module.eks.cluster_endpoint
}

output "ecr_registry" {
  description = "Host del registry ECR de la cuenta/región."
  value       = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}

output "ecr_repository_urls" {
  description = "URL de cada repositorio ECR por nombre de imagen."
  value       = { for name, repo in module.repository : name => repo.repository_url }
}

output "true_native_secret_token" {
  description = "SECRET_TOKEN de TrueNative (entrega 3). No es un credential real, ver variables.tf."
  value       = var.true_native_secret_token
  sensitive   = true
}

output "notifications_sns_topic_arn" {
  description = "ARN del Topic de SNS de notificaciones (SNS_TOPIC_ARN de notifications_app)."
  value       = module.notifications_sns.topic_arn
}

output "credit_cards_internal_secret" {
  description = "Token de servicio del endpoint interno de tarjetas."
  value       = var.credit_cards_internal_secret
}
