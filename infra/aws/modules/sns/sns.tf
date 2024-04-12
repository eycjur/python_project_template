# SNSで使用するトピックと通知先を作成する

resource "aws_sns_topic" "nortification-email" {
  name = "nortification-email"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.nortification-email.arn
  protocol  = "email"
  endpoint  = var.env["MAIL_ADDRESS"]
}

output "sns_topic_arn" {
  value = aws_sns_topic.nortification-email.arn
}
