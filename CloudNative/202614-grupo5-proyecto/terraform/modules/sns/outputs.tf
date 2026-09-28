output "topic_arn" {
  description = "ARN del Topic de SNS."
  value       = aws_sns_topic.this.arn
}
