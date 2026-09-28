# Política de ciclo de vida: conserva solo las últimas N imágenes.
locals {
  policy_document = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Conservar las últimas ${var.keep_tags_number} imágenes"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = var.keep_tags_number
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
