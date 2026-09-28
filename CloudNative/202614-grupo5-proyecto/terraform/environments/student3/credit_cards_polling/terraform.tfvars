aws_region   = "us-east-1"
owner        = "ga.gonzalezo1"
cluster_name = "clonatdevs-eks"

# Mismo valor que en terraform/environments/student3/apps/terraform.tfvars.
true_native_secret_token = "rf007-truenative-shared-secret"

# lambda_enabled ya es true por defecto (ver terraform/stacks/credit_cards_polling/variables.tf).
# Sobreescribir aqui solo si este ambiente necesita desactivarla temporalmente.
