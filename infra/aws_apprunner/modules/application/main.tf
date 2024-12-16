# ECRリポジトリの作成とApp Runnerのアプリケーション構築を行うためのモジュール

resource "aws_ecr_repository" "ecr" {
  name                 = var.setting.container_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# 初回実行時はコンテナがないと起動に失敗するため、イメージを置いておく
# Note: ローカルの状態に依存するので、失敗前提で適当なコンテナを利用しても良い
resource "null_resource" "tmp_image" {
  provisioner "local-exec" {
    command = <<BASH
      aws ecr get-login-password --region ${var.common.aws_region} | docker login --username AWS --password-stdin ${var.common.aws_account_id}.dkr.ecr.${var.common.aws_region}.amazonaws.com
      docker buildx build \
        --platform linux/amd64 \
        --tag ${var.common.aws_account_id}.dkr.ecr.${var.common.aws_region}.amazonaws.com/${var.setting.container_name}:latest \
        --push \
        ../../.
    BASH
  }
}

resource "aws_apprunner_service" "app_runner" {
  service_name = var.setting.container_name

  source_configuration {
    authentication_configuration {
      access_role_arn = "arn:aws:iam::${var.common.aws_account_id}:role/service-role/AppRunnerECRAccessRole"
    }
    image_repository {
      image_configuration {
        port = var.setting.container_port
        runtime_environment_variables = {
          CONTAINER_PORT                 = var.setting.container_port
          AWS_SECRET_MANAGER_SECRET_NAME = var.setting.secret_name
        }
      }
      image_identifier      = "${aws_ecr_repository.ecr.repository_url}:latest"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = true
  }
  instance_configuration {
    cpu               = 1024
    memory            = 2048
    instance_role_arn = var.setting.instance_role_arn
  }
}
