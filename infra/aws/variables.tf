locals {
  common = {
    aws_account_id = "389376010567"
    aws_region     = "ap-northeast-1"
  }

  db = {
    table_name_histories = "dynamodb_table_histories"
  }

  application = {
    instance_role_arn = module.iam.role_arn
    container_name    = "python-project-template"
    container_port    = 5678
  }
}
