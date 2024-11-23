resource "aws_wafv2_ip_set" "main" {
  name               = var.setting.ip_set_name
  scope              = "REGIONAL"
  ip_address_version = "IPV4"
  addresses          = ["${var.setting.ip_address}/32"]
}

resource "aws_wafv2_web_acl" "main" {
  name  = var.setting.web_acl_name
  scope = "REGIONAL"

  default_action {
    block {}
  }

  rule {
    name     = "allow"
    priority = 1

    action {
      allow {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.main.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = var.setting.rule_metric_name
      sampled_requests_enabled   = false
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = false
    metric_name                = var.setting.metric_name
    sampled_requests_enabled   = true
  }
}

# HTTP APIはWAF未対応
# https://repost.aws/questions/QUXjJnNPjoRgqgwSs-5jbMjw?newRedirect=1&messageID=942361
# resource "aws_wafv2_web_acl_association" "main" {
#   resource_arn = var.setting.api_gateway_arn
#   web_acl_arn  = aws_wafv2_web_acl.main.arn
# }
