output "url" {
  value = "${aws_apigatewayv2_api.main.api_endpoint}/${aws_apigatewayv2_stage.main.name}/"
}
