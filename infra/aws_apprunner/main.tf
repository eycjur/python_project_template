module "iam" {
  source = "./modules/iam"
}

module "application" {
  source = "./modules/application"

  common  = local.common
  setting = local.application
}

module "db" {
  source = "./modules/db"

  common  = local.common
  setting = local.db
}

module "monitoring" {
  source = "./modules/monitoring"

  common  = local.common
  setting = local.monitoring
}

module "secret_manager" {
  source = "./modules/secret_manager"

  common  = local.common
  setting = local.secret_manager
}
