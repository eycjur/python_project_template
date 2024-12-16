data "dotenv" "config" {
  filename = "../../.env"
}

locals {
  app_name = "python-project-template"

  common = {
    aws_account_id = data.dotenv.config.env["AWS_ACCOUNT_ID"]
    aws_region     = "ap-northeast-1"
  }

  db = {
    table_name_histories = "dynamodb_table_histories"
  }

  application = {
    repository_name            = local.app_name
    function_name              = local.app_name
    role_arn                   = module.iam.role_arn
    api_gateway_name           = join("-", [local.app_name, "api-gateway"])
    stage_name                 = "dev"
    secret_name                = module.secret_manager.secret_name
    api_gateway_log_group_name = "/api-gateway-log"
    env                        = data.dotenv.config.env
  }

  ip_restriction = {
    ip_address       = data.dotenv.config.env["IP_ADDRESS"]
    ip_set_name      = join("-", [local.app_name, "ip-set"])
    web_acl_name     = join("-", [local.app_name, "web-acl"])
    rule_metric_name = join("-", [local.app_name, "web-acl-metric", "rule"])
    metric_name      = join("-", [local.app_name, "web-acl-metric"])
    api_gateway_arn  = module.application.api_gateway_arn
  }

  monitoring = {
    email_address = data.dotenv.config.env["EMAIL_ADDRESS"]
  }

  secret_manager = {
    secret_name = join("-", [local.app_name, "secret"])
  }
}
