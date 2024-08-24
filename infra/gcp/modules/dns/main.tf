resource "google_dns_managed_zone" "main" {
  name       = var.setting.zone_name
  dns_name   = "${var.setting.domain}." # DNS 名のサフィックス。末尾に "." が必須
  visibility = "public"

  dnssec_config {
    state = "on"
  }
}

resource "google_dns_record_set" "main" {
  name         = "${var.setting.domain}."
  managed_zone = google_dns_managed_zone.main.name
  type         = "A"
  ttl          = 0
  rrdatas      = var.setting.rrdatas
}
