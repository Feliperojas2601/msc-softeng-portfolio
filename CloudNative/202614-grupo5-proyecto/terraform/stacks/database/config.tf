provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      terraform = true
      owner     = var.owner
      project   = "202614-grupo5-proyecto"
      stack     = "database"
    }
  }
}

terraform {
  required_version = "~> 1.12"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3"
    }
  }

  backend "s3" {}
}
