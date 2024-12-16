terraform {
  required_version = "~> 1.5.0"

  backend "gcs" {
    bucket = "eycjur-terraform-state-bucket"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.38.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.2"
    }
    dotenv = {
      source  = "jrhouston/dotenv"
      version = "~> 1.0"
    }
  }
}

provider "google" {
  project = local.common.project_id
  region  = local.common.region
}
