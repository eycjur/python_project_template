output "app_runner_service_url" {
  value = module.application.app_runner_service_url
}

output "AWS_ACCOUNT_ID" {
  value = local.common.aws_account_id
}

output "AWS_REGION" {
  value = local.common.aws_region
}

output "AWS_DYNAMODB_TABLE_NAME_HISTORIES" {
  value = local.db.table_name_histories
}

output "AWS_SECRET_MANAGER_SECRET_NAME" {
  value = module.secret_manager.secret_name
}
