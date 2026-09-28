aws_region                     = "us-east-1"
owner                          = "g.zambranoz"
cluster_name                   = "clonatdevs-eks"
k8s_cluster_version            = "1.33"
cluster_endpoint_public_access = true
node_instance_types            = ["t3.medium"]
node_desired_size              = 2
node_min_size                  = 1
node_max_size                  = 3
keep_tags_number               = 5

# No es un credential real, ver comentario en terraform/stacks/apps/variables.tf
true_native_secret_token       = "rf007-truenative-shared-secret"
credit_cards_internal_secret   = "rf006-credit-cards-internal-secret"
