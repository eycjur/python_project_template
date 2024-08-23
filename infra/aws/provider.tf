terraform {
  required_version = "~> 1.5.0"

  backend "s3" {
    bucket = "eycjur-terraform-state-bucket"
    key    = "terraform/state/terraform.tfstate"
    region = "ap-northeast-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    dotenv = {
      source  = "jrhouston/dotenv"
      version = "~> 1.0"
    }
  }
}

provider "aws" {
  region = local.common.aws_region
}
