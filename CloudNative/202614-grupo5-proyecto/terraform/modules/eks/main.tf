# Clúster EKS sobre la VPC por defecto, reutilizando los roles del Learner Lab.
module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.31"

  cluster_name    = var.cluster_name
  cluster_version = var.k8s_cluster_version
  vpc_id          = data.aws_vpc.default.id
  subnet_ids      = data.aws_subnets.all.ids

  cluster_endpoint_public_access = var.cluster_endpoint_public_access

  create_iam_role = false
  iam_role_arn    = local.cluster_role_arn

  eks_managed_node_groups = {
    default = {
      create_iam_role = false
      iam_role_arn    = local.node_role_arn
      ami_type        = "AL2023_x86_64_STANDARD"
      instance_types  = var.node_instance_types
      desired_size    = var.node_desired_size
      min_size        = var.node_min_size
      max_size        = var.node_max_size
    }
  }

  node_security_group_additional_rules = {
    egress_rds_postgres = {
      description = "Nodos a RDS PostgreSQL"
      type        = "egress"
      protocol    = "tcp"
      from_port   = 5432
      to_port     = 5432
      cidr_blocks = [data.aws_vpc.default.cidr_block]
    }

    # Las "recommended rules" del modulo v18 solo abren 443 y 10250 desde el
    # control plane. Los webhooks de admision escuchan en otros puertos (p.ej.
    # ingress-nginx en 8443), asi que el API server no los alcanza y todo
    # `create ingress` falla con "failed calling webhook ... context deadline
    # exceeded". Esta es la regla recomendada por AWS para ese caso.
    ingress_cluster_webhooks = {
      description                   = "Control plane a webhooks de admision en los nodos"
      type                          = "ingress"
      protocol                      = "tcp"
      from_port                     = 1025
      to_port                       = 65535
      source_cluster_security_group = true
    }

    # Las "recommended rules" de v18 solo permiten trafico nodo-a-nodo en el
    # puerto 53 (CoreDNS). Con el VPC CNI cada pod tiene IP de la VPC y el
    # trafico pod-a-pod entre nodos pasa por sus ENI, filtrado por este SG:
    # sin estas reglas, un pod en un nodo no alcanza a un pod en el otro
    # (los Service de dominio dan timeout -> 504/503). "Permitir todo entre
    # nodos del mismo grupo" es lo que trae EKS por defecto.
    ingress_self_all = {
      description = "Trafico pod-a-pod entre nodos"
      type        = "ingress"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      self        = true
    }

    egress_self_all = {
      description = "Trafico pod-a-pod entre nodos"
      type        = "egress"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      self        = true
    }
  }

  aws_auth_roles = [
    {
      rolearn  = local.lab_role_arn
      username = "system:node:{{EC2PrivateDNSName}}"
      groups   = ["system:bootstrappers", "system:nodes"]
    },
    {
      rolearn  = local.lab_role_arn
      username = "lab-admin"
      groups   = ["system:masters"]
    },
  ]

  enable_irsa               = false
  create_aws_auth_configmap = false
  manage_aws_auth_configmap = false
}
