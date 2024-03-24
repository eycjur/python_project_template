resource "aws_ecr_repository" "ecr" {
  name                 = var.env["CONTAINER_NAME"]
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr.repository_url
}
