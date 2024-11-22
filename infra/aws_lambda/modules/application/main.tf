# lambdaの関数とECRリポジトリとAPI Gatewayを作成するためのモジュール

resource "aws_ecr_repository" "main" {
  name = var.setting.repository_name
}

# 初回実行時はコンテナがないと起動に失敗するため、イメージを置いておく
# Note: ローカルの状態に依存するので、失敗前提で適当なコンテナを利用しても良い
resource "null_resource" "tmp_image" {
  provisioner "local-exec" {
    command = <<BASH
      aws ecr get-login-password --region ${var.common.aws_region} | docker login --username AWS --password-stdin ${var.common.aws_account_id}.dkr.ecr.${var.common.aws_region}.amazonaws.com
      docker buildx build \
        --platform linux/amd64 \
        --tag ${var.common.aws_account_id}.dkr.ecr.${var.common.aws_region}.amazonaws.com/${var.setting.repository_name}:latest \
        --push \
        --provenance=false \
        --file ../../Dockerfile.lambda \
        ../../.
    BASH
  }
}

resource "aws_lambda_function" "main" {
  function_name = var.setting.function_name
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.main.repository_url}:latest"
  role          = var.setting.lambda_role_arn
  memory_size   = 512
  timeout       = 600

  environment {
    variables = {
      AWS_SECRET_MANAGER_SECRET_NAME = var.setting.secret_name
    }
  }

  lifecycle {
    ignore_changes = [image_uri]
  }

  depends_on = [null_resource.tmp_image]
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${var.common.aws_region}:${var.common.aws_account_id}:${aws_apigatewayv2_api.main.id}/*/*/*"
}

resource "aws_apigatewayv2_api" "main" {
  name          = var.setting.api_gateway_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "main" {
  api_id           = aws_apigatewayv2_api.main.id
  integration_type = "AWS_PROXY"

  connection_type    = "INTERNET"
  integration_method = "POST"
  integration_uri    = aws_lambda_function.main.invoke_arn
}

resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_apigatewayv2_route" "other" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_cloudwatch_log_group" "api_gateway_log" {
  name = "/api-gateway-log"

  retention_in_days = 7
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  auto_deploy = true
  name        = var.setting.stage_name

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_log.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }

  default_route_settings {
    data_trace_enabled       = true
    detailed_metrics_enabled = true

    throttling_burst_limit = 500
    throttling_rate_limit  = 100
  }
}
