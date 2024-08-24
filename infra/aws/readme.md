# AWS Infrastructure

Terraformを用いたAWSのインフラ構築

## 実施手順

### 前準備

1. Terraform State用のS3バケット作成
    - Amazon S3 > バケットを作成 の画面から、terraform-state保存用のS3バケット（ex. `<app_name>-terraform-state-bucket`）を作成  
        バケットタイプは汎用、ACLは無効、パブリックアクセスはブロック、バージョニングは無効、暗号化はS3マネージドキーを選択

### Terraformコマンドの実行

```bash
make create-infra-aws
```

### 後処理

1. SNSトピックにサブスクリプションを追加
    - Amazon SNS > 該当トピック > サブスクリプション の画面から、プロトコルはEメール、エンドポイントは通知を受け取るメールアドレスを入力してサブスクリプションを追加
    - ※メールアドレスをTerraformで管理したくないので、手動で追加する
