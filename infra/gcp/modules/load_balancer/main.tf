# クライアントリクエスト処理の概要
# 1. クライアントのリクエストは、まずロードバランサーのエントリーポイント（google_compute_global_addressで設定されたIPアドレス）に送信されます。
# 2. ロードバランサーのフロントエンド（google_compute_global_forwarding_rule）がリクエストを受信し、ターゲットプロキシ（google_compute_target_https_proxy）へルーティングします。
# 3. ターゲットプロキシでクライアントとの接続が終端され、URLマップ（google_compute_url_map）に基づいて、適切なバックエンドサービス（google_compute_backend_service）へ新しい接続が作成されます（プロキシロードバランシング方式）。
# 4. バックエンドサービスはネットワークエンドポイントグループ（google_compute_region_network_endpoint_group）を介して、Cloud Run サービスにリクエストを渡します。
# ※ サービスの作成手順は依存関係の都合上、逆順で記載しています。


# バックエンドサービスの設定
resource "google_compute_backend_service" "main" {
  name = var.setting.backend_service_name

  # 外部からのトラフィックはHTTPSで受け取り、内部のロードバランサとバックエンドサービス間の通信はHTTPを使用
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30
  security_policy       = var.setting.security_policy_id

  backend {
    group = resource.google_compute_region_network_endpoint_group.main.id
  }

  lifecycle {
    create_before_destroy = true
  }
}

# ネットワークエンドポイントグループの設定
resource "google_compute_region_network_endpoint_group" "main" {
  name                  = var.setting.neg_name
  network_endpoint_type = "SERVERLESS"
  region                = var.common.region
  cloud_run {
    service = var.setting.neg_backend_name
  }
}

# リクエストを適切なバックエンドにルーティングするためのURLマップを定義
resource "google_compute_url_map" "main" {
  name            = var.setting.url_map_name
  default_service = google_compute_backend_service.main.id
}

# SSL証明書用に、名前が被らないようにランダムな名前を生成
resource "random_id" "certificate_name" {
  byte_length = 4
  prefix      = "${var.setting.ssl_certificate_name}-"

  # これが変更されると、ランダムな名前が再生成される
  keepers = {
    domains = var.setting.domain
  }
}

# SSL証明書の発行
resource "google_compute_managed_ssl_certificate" "main" {
  name = random_id.certificate_name.hex
  type = "MANAGED"
  managed {
    domains = [var.setting.domain]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# HTTPS プロキシ
# クライアントからのHTTPSリクエストを受け取り、それをロードバランサーのバックエンドサービスに転送
resource "google_compute_target_https_proxy" "main" {
  name = var.setting.https_proxy_name

  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

# グローバルロードバランサ用のグローバル IPv4 アドレス
resource "google_compute_global_address" "main" {
  name         = var.setting.ip_address_name
  address_type = "EXTERNAL"
}

# ロードバランサのフロントエンド（IP アドレスと HTTPS プロキシをマッピング）
resource "google_compute_global_forwarding_rule" "main" {
  name                  = var.setting.forwarding_rule_name
  load_balancing_scheme = "EXTERNAL_MANAGED"
  ip_protocol           = "TCP"

  target     = google_compute_target_https_proxy.main.id
  port_range = "443"
  ip_address = google_compute_global_address.main.id
}
