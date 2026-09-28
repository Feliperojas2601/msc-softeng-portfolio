module "eks" {
  source = "../../modules/eks"

  cluster_name                   = var.cluster_name
  k8s_cluster_version            = var.k8s_cluster_version
  cluster_endpoint_public_access = var.cluster_endpoint_public_access
  node_instance_types            = var.node_instance_types
  node_desired_size              = var.node_desired_size
  node_min_size                  = var.node_min_size
  node_max_size                  = var.node_max_size
}

module "repository" {
  source   = "../../modules/repository"
  for_each = toset(local.ecr_repositories)

  repository_name  = each.key
  keep_tags_number = var.keep_tags_number
}

module "notifications_sns" {
  source = "../../modules/sns"

  topic_name         = "clonatdevs-notifications"
  email_subscription = local.email_to_notify
}
