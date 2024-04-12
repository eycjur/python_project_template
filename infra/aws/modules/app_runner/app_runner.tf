# App Runner によるコンテナデプロイメントを行うためのモジュール

# 初回実行時はコンテナがないと機動に失敗するため、イメージを置いておく
resource "null_resource" "tmp_image" {
  provisioner "local-exec" {
    command = <<BASH
      aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
      docker buildx build \
        --platform linux/amd64 \
        --tag $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$CONTAINER_NAME:latest \
        --push \
        ../../.
    BASH

    environment = var.env
  }
}

resource "aws_apprunner_service" "app_runner" {
  service_name = var.env["CONTAINER_NAME"]

  source_configuration {
    authentication_configuration {
      access_role_arn = "arn:aws:iam::${var.env["AWS_ACCOUNT_ID"]}:role/service-role/AppRunnerECRAccessRole"
    }
    image_repository {
      image_configuration {
        port                          = var.env["CONTAINER_PORT"]
        runtime_environment_variables = var.env
      }
      image_identifier      = "${var.ecr_repository_url}:latest"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = true
  }
  instance_configuration {
    cpu               = 1024
    memory            = 2048
    instance_role_arn = var.instance_role_arn
  }
}

output "app_runner_service_url" {
  value = aws_apprunner_service.app_runner.service_url
}
