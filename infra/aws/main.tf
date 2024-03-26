data "dotenv" "config" {
  filename = "../../.env"
}

provider "aws" {
  region = data.dotenv.config.env["AWS_REGION"]
}

module "iam" {
  source = "./modules/iam"
}

module "ecr" {
  source = "./modules/ecr"

  env = data.dotenv.config.env
}

module "dynamodb" {
  source = "./modules/dynamodb"

  env = data.dotenv.config.env
}

module "app_runner" {
  source = "./modules/app_runner"

  env = data.dotenv.config.env
  instance_role_arn = module.iam.role_arn
  ecr_repository_url = module.ecr.ecr_repository_url
}
