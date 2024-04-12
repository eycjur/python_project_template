variable "env" {
  type = map(any)
}

variable "instance_role_arn" {
  type = string
}

variable "ecr_repository_url" {
  type = string
}
