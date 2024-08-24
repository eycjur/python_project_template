# Cloud Runで使用するサービスアカウンを作成する
resource "google_service_account" "main" {
  project      = var.common.project_id
  account_id   = var.setting.account
  display_name = var.setting.display_name
}

# IAM ロールバインド
resource "google_project_iam_member" "main" {
  project = var.common.project_id
  member  = "serviceAccount:${google_service_account.main.email}"
  role    = var.setting.role
}
