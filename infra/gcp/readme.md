# AWS Infrastructure

Terraformを用いたAWSのインフラ構築

## 実施手順

### 前準備

1. Terraform State用のGCSバケット作成
    - Cloud Storage > バケット の画面から、terraform-state保存用のGCSバケット（ex. `<app_name>-terraform-state-bucket`）を作成  
        保存場所やストレージクラスは任意、公開アクセスの防止はオンを選択

### Terraformコマンドの実行

```bash
make create-infra-gcp
```

### 後処理

1. サービスアカウントキーの発行
    - IAMと管理 > サービスアカウント > 作成したサービスアカウント > キー の画面から、 鍵を追加 > 新しい鍵の作成 > JSON > 作成 で鍵を作成してダウンロード
    - credentials/credential_gcp.jsonとして保存
1. ドメインの発行
    - Cloud Domains > ドメインを登録 からドメインを発行
    - DNSはterraformで作成したCloud DNSのゾーンを指定
2. SSL証明書のプロビジョニング
    - セキュリティ > Certificate Manager > 従来の証明書 の画面からステータスが完了になるまで待つ
1. makeコマンドでデプロイ
    - make deploy-gcpコマンドを実行すると、アプリケーションのデプロイが行われます
1. 通知チャンネルの作成
    - Monitoring > アラート > EDIT NOTIFICATION CHANNELS から、Emailの通知チャンネルを作成
    - アラートポリシーを編集し、作成した通知チャンネルを追加
