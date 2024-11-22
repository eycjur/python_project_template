locals {
  app_name = "python-project-template"

  common = {
    aws_account_id = "389376010567"
    aws_region     = "ap-northeast-1"
  }

  db = {
    table_name_histories = "dynamodb_table_histories"
  }

  application = {
    repository_name            = local.app_name
    function_name              = local.app_name
    lambda_role_arn            = module.iam.role_arn
    api_gateway_name           = join("-", [local.app_name, "api-gateway"])
    stage_name                 = "dev"
    secret_name                = module.secret_manager.secret_name
    api_gateway_log_group_name = "/api-gateway-log"
  }

  secret_manager = {
    secret_name = join("-", [local.app_name, "secret"])
  }
}
