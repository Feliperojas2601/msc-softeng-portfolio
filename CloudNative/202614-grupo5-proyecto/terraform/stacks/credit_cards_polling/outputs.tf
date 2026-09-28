output "lambda_arn" {
  description = "ARN de la Lambda de polling cuando está habilitada."
  value       = module.credit_cards_polling_lambda.lambda_arn
}
