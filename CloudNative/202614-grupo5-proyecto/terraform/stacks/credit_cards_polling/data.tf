data "aws_caller_identity" "current" {}

# Cluster creado por el stack apps (corre antes en tf_stacks); se identifica
# por nombre, no por estado remoto, para no acoplar los dos stacks.
data "aws_eks_cluster" "this" {
  name = var.cluster_name
}

data "aws_eks_cluster_auth" "this" {
  name = var.cluster_name
}

# Misma cola creada por el stack apps (modulo credit_cards_queue), buscada
# por nombre para no depender de su estado remoto.
data "aws_sqs_queue" "polling" {
  name = "clonatdevs-credit-cards-polling"
}

# Reutilizados para la Lambda, igual que en el módulo eks: no se permite
# crear roles IAM nuevos en Academy, solo reutilizar LabRole y la VPC default.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "availability-zone"
    values = ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d"]
  }
}

data "aws_iam_roles" "lab_role" {
  name_regex = "LabRole"
}

# Balanceadores internos creados por k8s_manifests
# (k8s/aws/credit_cards_polling_connectivity.yml), ya desplegados cuando este
# stack corre (post_k8s_stacks se aplica después de k8s_manifests).
data "kubernetes_service_v1" "lambda_connectivity" {
  for_each = var.lambda_enabled ? local.lambda_connectivity_service_names : {}

  metadata {
    name      = each.value
    namespace = "default"
  }
}
