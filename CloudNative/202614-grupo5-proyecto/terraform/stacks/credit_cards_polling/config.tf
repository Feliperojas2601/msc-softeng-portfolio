provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      terraform = true
      owner     = var.owner
      project   = "202614-grupo5-proyecto"
      stack     = "credit_cards_polling"
    }
  }
}

# El cluster EKS ya existe (lo crea el stack apps, que corre antes). Este
# stack solo lo consulta para autenticar el provider kubernetes contra el
# mismo cluster y leer los balanceadores internos ya desplegados por
# k8s_manifests (ver data.tf).
provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.this.token
}

terraform {
  required_version = "~> 1.12"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }

  backend "s3" {}
}
