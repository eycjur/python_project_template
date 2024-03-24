terraform {
  required_version = "~> 1.5.0"

  backend "local" {
    path = "./terraform.tfstate"
  }

  required_providers {
    dotenv = {
      source  = "jrhouston/dotenv"
      version = "~> 1.0"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
