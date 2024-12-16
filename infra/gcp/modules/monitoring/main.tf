resource "google_monitoring_alert_policy" "main" {
  display_name = var.setting.alert_policy_name
  combiner     = "OR"
  severity     = "ERROR"
  documentation {
    content = "Cloud Runでエラーが発生しました"
  }

  notification_channels = [google_monitoring_notification_channel.main.name]

  conditions {
    display_name = var.setting.condition_display_name
    condition_matched_log {
      filter = var.setting.filter
    }
  }

  alert_strategy {
    notification_rate_limit {
      period = "3600s"
    }
    auto_close = "604800s" # 7 days
  }
}

resource "google_monitoring_notification_channel" "main" {
  type = "email"
  labels = {
    email_address = var.setting.email_address
  }
}
