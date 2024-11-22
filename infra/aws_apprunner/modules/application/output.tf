output "app_runner_service_url" {
  value = "https://${aws_apprunner_service.app_runner.service_url}"
}
