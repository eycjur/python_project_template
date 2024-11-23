output "url" {
  value = "${aws_apigatewayv2_stage.main.invoke_url}/"
}

output "api_gateway_arn" {
  value = aws_apigatewayv2_stage.main.arn
}
