output "AWS_ACCOUNT_ID" {
  value = local.common.aws_account_id
}

output "AWS_REGION" {
  value = local.common.aws_region
}

output "AWS_DYNAMODB_TABLE_NAME_HISTORIES" {
  value = local.db.table_name_histories
}

output "AWS_LAMBDA_ROLE" {
  value = module.iam.role_arn
}

output "AWS_SECRET_MANAGER_SECRET_NAME" {
  value = module.secret_manager.secret_name
}

output "AWS_API_GATEWAY_STAGE_NAME" {
  value = local.application.stage_name
}

output "application_url" {
  value = module.application.url
}
