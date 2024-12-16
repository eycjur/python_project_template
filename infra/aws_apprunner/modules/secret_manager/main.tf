resource "aws_secretsmanager_secret" "main" {
  name = var.setting.secret_name
}
