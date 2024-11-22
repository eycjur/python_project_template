# SNSで使用するトピックと通知先を作成する

resource "aws_sns_topic" "nortification-email" {
  name = "nortification-email"
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
  alarm_actions             = [aws_sns_topic.nortification-email.arn]
}
