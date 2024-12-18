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
    instance_role_arn = module.iam.role_arn
    container_name    = "python-project-template"
    container_port    = 5678
    secret_name       = module.secret_manager.secret_name
  }

  monitoring = {
    email_address = data.dotenv.config.env["EMAIL_ADDRESS"]
  }

  secret_manager = {
    secret_name = join("-", [local.app_name, "secret"])
  }
}
