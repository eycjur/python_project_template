data "dotenv" "config" {
  filename = "../../.env"
}

locals {
  app_name = "python-project-template"

  common = {
    project_id = data.dotenv.config.env["GCP_PROJECT_ID"]
    region     = "asia-northeast1"
  }

  apis_to_enable = [
    "certificatemanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
    "dns.googleapis.com",
    "domains.googleapis.com",
    "firestore.googleapis.com",
    "iam.googleapis.com",
    "run.googleapis.com",
    "storage-component.googleapis.com",
    "secretmanager.googleapis.com",
  ]

  db = {
    name = "firestore-db-history"
  }

  application = {
    service_name = "python-project-template"
    # 初期構築のみで使用するため、適当なイメージを指定
    container_image = "nginx:latest"
    container_port  = 80
    ingress         = "INGRESS_TRAFFIC_ALL" # INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER
    secret_id       = module.secret_manager.secret_id
  }

  iam = {
    account      = "sa-for-all"
    display_name = "Service Account for All"
    roles        = ["roles/editor", "roles/secretmanager.secretAccessor"]
  }

  monitoring = {
    alert_policy_name      = "Error Alert Policy"
    condition_display_name = "Cloud Run Error"
    filter                 = "resource.type=\"cloud_run_revision\" AND severity=\"ERROR\""
    email_address          = data.dotenv.config.env["EMAIL_ADDRESS"]
  }

  secret_manager = {
    secret_name = join("-", [local.app_name, "env"])
  }

  # dns = {
  #   domain    = "eycjur-python-project-template.com"
  #   zone_name = "zone"
  #   rrdatas   = [module.load_balancer.ip_address]
  # }

  # ip_restriction = {
  #   name          = "ip-restriction"
  #   src_ip_ranges = [data.dotenv.config.env["IP_ADDRESS"]]
  # }

  # load_balancer = {
  #   domain               = "eycjur-python-project-template.com"
  #   dns_zone_name        = "zone"
  #   ssl_certificate_name = "ssl-certificate"
  #   ip_address_name      = "ip-address"
  #   security_policy_id   = module.ip_restriction.security_policy_id
  #   backend_service_name = "backend-service"
  #   neg_name             = "network-endpoint-group"
  #   neg_backend_name     = local.application.service_name
  #   url_map_name         = "url-map"
  #   https_proxy_name     = "https-proxy"
  #   forwarding_rule_name = "forwarding-rule"
  # }
}
