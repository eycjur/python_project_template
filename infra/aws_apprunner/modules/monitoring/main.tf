# SNSで使用するトピックと通知先を作成する

resource "aws_sns_topic" "notification-email" {
  name = "notification-email"
  #trivy:ignore:AVD-AWS-0136  # マネージドキーで十分
  kms_master_key_id = "alias/aws/sns"
}

resource "aws_sns_topic_subscription" "main" {
  topic_arn = aws_sns_topic.notification-email.arn
  protocol  = "email"
  endpoint  = var.setting.email_address
}


# CloudWatchでログを監視するためのリソースを定義する

resource "aws_cloudwatch_log_group" "application" {
  name = "/application" // logger_config_aws.yamlの設定に合わせる
}

resource "aws_cloudwatch_log_stream" "python" {
  name           = "python" // logger_config_aws.yamlの設定に合わせる
  log_group_name = aws_cloudwatch_log_group.application.name
}

resource "aws_cloudwatch_log_metric_filter" "error_filter" {
  name           = "error"
  pattern        = "%ERROR|CRITICAL%"
  log_group_name = aws_cloudwatch_log_group.application.name

  metric_transformation {
    name      = "ErrorCount"
    namespace = "Application"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "error_alarm" {
  alarm_name                = "application-error-alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "ErrorCount"
  namespace                 = "Application"
  period                    = 60
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "This metric monitors the error logs"
  insufficient_data_actions = []
  alarm_actions             = [aws_sns_topic.notification-email.arn]
}
