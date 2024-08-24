resource "google_compute_security_policy" "main" {
  name        = var.setting.name
  description = "IP制限"

  rule {
    action   = "deny(403)"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }

  rule {
    action   = "allow"
    priority = "0"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = var.setting.src_ip_ranges
      }
    }
  }
}
