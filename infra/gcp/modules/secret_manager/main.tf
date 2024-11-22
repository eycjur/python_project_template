resource "google_secret_manager_secret" "main" {
  secret_id = var.setting.secret_name

  replication {
    auto {}
  }
}
