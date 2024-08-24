# Sevice APIの有効化
resource "google_project_service" "api_activation" {
  provider                   = google
  project                    = local.common.project_id
  disable_dependent_services = false
  disable_on_destroy         = false

  for_each = toset(local.apis_to_enable)
  service  = each.value
}

module "iam" {
  source = "./modules/iam"

  common  = local.common
  setting = local.iam
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

module "ip_restriction" {
  source = "./modules/ip_restriction"

  common  = local.common
  setting = local.ip_restriction
}

module "dns" {
  source = "./modules/dns"

  common  = local.common
  setting = local.dns
}

module "load_balancer" {
  source = "./modules/load_balancer"

  common  = local.common
  setting = local.load_balancer
}

module "monitoring" {
  source = "./modules/monitoring"

  common  = local.common
  setting = local.monitoring
}
