data "aws_caller_identity" "current" {}

# EMAIL_TO_NOTIFY llega por Secrets Manager, no como -var de Terraform: el
# pipeline replica el secret de GitHub del mismo nombre dentro de
# secrets-pipeline-native-map (ver "Notificaciones por correo" en el README
# de la raiz). Leerlo asi evita el problema de "secret poisoning" en
# tf_outputs que ya se dio con TRUE_NATIVE_SECRET_TOKEN: este valor nunca
# pasa por un output de Terraform ni por un output de job de GitHub Actions.
data "aws_secretsmanager_secret" "pipeline_native_map" {
  name = "secrets-pipeline-native-map"
}

data "aws_secretsmanager_secret_version" "pipeline_native_map" {
  secret_id = data.aws_secretsmanager_secret.pipeline_native_map.id
}
