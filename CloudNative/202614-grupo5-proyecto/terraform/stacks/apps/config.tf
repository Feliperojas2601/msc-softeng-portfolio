provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      terraform = true
      owner     = var.owner
      project   = "202614-grupo5-proyecto"
      stack     = "apps"
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
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2"
    }
  }

  backend "s3" {}
}
