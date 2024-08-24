resource "google_firestore_database" "main" {
  project                           = var.common.project_id
  name                              = var.setting.name
  location_id                       = var.common.region
  type                              = "FIRESTORE_NATIVE"
  point_in_time_recovery_enablement = "POINT_IN_TIME_RECOVERY_ENABLED"
  delete_protection_state           = "DELETE_PROTECTION_ENABLED"
  deletion_policy                   = "ABANDON"
}

resource "google_firestore_backup_schedule" "weekly-backup" {
  project  = var.common.project_id
  database = google_firestore_database.main.name

  retention = "8467200s" // 14 weeks (maximum possible retention)

  weekly_recurrence {
    day = "SUNDAY"
  }
}
