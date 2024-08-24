resource "google_cloud_run_v2_service" "main" {
  name     = var.setting.service_name
  location = var.common.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    containers {
      image = var.setting.container_image
      ports {
        container_port = var.setting.container_port
      }
    }
  }

  # Cloud Runのデプロイはmakeコマンドにて行うので、初期構築後の差分は無視する
  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers,
      template[0].revision,
    ]
  }
}

# 未認証の呼び出しを許可
resource "google_cloud_run_v2_service_iam_member" "main" {
  location = google_cloud_run_v2_service.main.location
  name     = google_cloud_run_v2_service.main.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_artifact_registry_repository" "main" {
  location      = var.common.region
  repository_id = var.setting.service_name
  format        = "DOCKER"
}
