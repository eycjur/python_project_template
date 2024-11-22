# Python Project Template
pythonでプロジェクトを作成する際のテンプレートです。

## Initialize Project

プロジェクトを初期化する際は、以下の手順で行ってください。

1. このリポジトリをクローン
2. .env.sampleを元に.envを作成
3. 不要なファイルを削除

### Minimize Project

本リポジトリは、各種クラウドでの動作確認等を行うため、最小限+αの構成としています。  
最小限の構成として利用する場合は、以下の手順で不要なファイルを削除してください。

1. `make minimize`を実行
2. docker-compose.ymlからcredentialsのマウントを削除
3. src/presentation/のサブディレクトリのうち、不要なフレームワークのディレクトリを削除
4. .devcontainer/devcontainer.jsonのlaunchの設定のうち、不要なフレームワークの設定を削除
5. README.mdを編集
6. クラウド関係の環境変数を.envとsrc/settings.pyから削除

## Run Application

アプリケーションを実行する際は、以下の手順で行ってください。

1. `make up`でDocker Composeを起動
2. http://localhost:<LOCAL_PORT>/ からアプリにアクセス
3. `make down`でDocker Composeを終了  
   終了せずにDev Containerを起動すると、docker-compose.override.ymlの内容が上書きされずデバッグが利用できません。

## Development

アプリケーションの開発を行う際は、以下の手順で行ってください。

1. pre-commitをインストール(ex. `pip install pre-commit`)
2. `pre-commit install`でpre-commitのhookスクリプトを導入
3. VSCodeでDev Container拡張機能をインストール
4. コマンドパレット(`Ctrl+Shift+P`)から`Remote-Containers: Reopen in Container`を実行
5. (Docker Compose立ち上げ時のみ)拡張機能の依存関係の解決に失敗することがあるので、ウィンドウの再読み込みする
6. F5でデバッグ実行が可能
7. http://localhost:<LOCAL_PORT>/ からアプリにアクセス

### FastAPI

FastAPIを利用する場合は、以下の手順で行ってください。

1. 上記手順でAPIサーバーを起動
2. live-server拡張機能で、src/presentation/fastapi/frontend/index.htmlを開く
3. http://localhost:5500/src/presentation/fastapi/frontend/ からフロントエンドにアクセス

## Deploy

各クラウドへのデプロイを行う際は、以下の手順で行ってください。

### GCP

#### 前準備

1. Terraform State用のGCSバケット作成
    - Cloud Storage > バケット の画面から、terraform-state保存用のGCSバケット（ex. `<app_name>-terraform-state-bucket`）を作成  
        保存場所やストレージクラスは任意、公開アクセスの防止はオンを選択

#### Terraformコマンドの実行

```bash
make create-infra-gcp
```

#### 後処理

1. サービスアカウントキーの発行
    - IAMと管理 > サービスアカウント > 作成したサービスアカウント > キー の画面から、 鍵を追加 > 新しい鍵の作成 > JSON > 作成 で鍵を作成してダウンロード
    - credentials/credential_gcp.jsonとして保存
1. ドメインの発行
    - Cloud Domains > ドメインを登録 からドメインを発行
    - DNSはterraformで作成したCloud DNSのゾーンを指定
1. SSL証明書のプロビジョニング
    - セキュリティ > Certificate Manager > 従来の証明書 の画面からステータスが完了になるまで待つ
1. makeコマンドでデプロイ
    - `make deploy-gcp`コマンドを実行すると、アプリケーションのデプロイが行われます
1. 通知チャンネルの作成
    - Monitoring > アラート > EDIT NOTIFICATION CHANNELS から、Emailの通知チャンネルを作成
    - アラートポリシーを編集し、作成した通知チャンネルを追加

#### リソースの削除

```bash
make destroy-gcp
```

### AWS App Runner

#### 前準備

1. Terraform State用のS3バケット作成
    - Amazon S3 > バケットを作成 の画面から、terraform-state保存用のS3バケット（ex. `<app_name>-terraform-state-bucket`）を作成  
        バケットタイプは汎用、ACLは無効、パブリックアクセスはブロック、バージョニングは無効、暗号化はS3マネージドキーを選択

#### Terraformコマンドの実行

```bash
make create-infra-aws-apprunner
```

#### 後処理

1. credentialsをcredentials/credentials_awsとして保存  
   ユーザーアカウントを利用する場合は`cp ~/.aws/credentials credentials/credentials_aws`としてください
1. `make deploy-aws-apprunner`でApp Runnerにデプロイ
1. SNSトピックにサブスクリプションを追加
    - Amazon SNS > 該当トピック > サブスクリプション の画面から、プロトコルはEメール、エンドポイントは通知を受け取るメールアドレスを入力してサブスクリプションを追加
    - ※メールアドレスをTerraformで管理したくないので、手動で追加する

#### リソースの削除

```bash
make destroy-aws-apprunner
```

### AWS Lambda

#### 前準備

1. Terraform State用のS3バケット作成
    - Amazon S3 > バケットを作成 の画面から、terraform-state保存用のS3バケット（ex. `<app_name>-terraform-state-bucket`）を作成  
        バケットタイプは汎用、ACLは無効、パブリックアクセスはブロック、バージョニングは無効、暗号化はS3マネージドキーを選択

#### Terraformコマンドの実行
    
```bash
make create-infra-aws-lambda
```

#### 後処理

1. credentialsをcredentials/credentials_awsとして保存  
   ユーザーアカウントを利用する場合は`cp ~/.aws/credentials credentials/credentials_aws`としてください
1. `make deploy-aws-lambda`でLambdaにデプロイ
1. SNSトピックにサブスクリプションを追加
    - Amazon SNS > 該当トピック > サブスクリプション の画面から、プロトコルはEメール、エンドポイントは通知を受け取るメールアドレスを入力してサブスクリプションを追加
    - ※メールアドレスをTerraformで管理したくないので、手動で追加する

#### リソースの削除

```bash
make destroy-aws-lambda
```

### Azure

Container Appsへのデプロイを実施します

1. Entra IDのアプリを登録からサービスプリンシパルを登録し、クライアントシークレットを発行する
2. .envのAZURE_CLIENT_ID,AZURE_CLIENT_SECRETに各値を設定
3. CosmosDBのデータベースとコレクションを作成
4. サービスプリンシパルにCosmosDBへのアクセス権の付与  
    ```shell
    az cosmosdb sql role assignment create \
    --account-name <CosmosDBのアカウント名> \
    --resource-group <リソースグループ名> \
    --scope "/" \
    --principal-id <EntraIDのエンタープライズアプリケーションの該当アプリケーション（サービスプリンシパル）のオブジェクトID> \
    --role-definition-id <ロールid=00000000-0000-0000-0000-000000000002>
   ```   
    cf. https://learn.microsoft.com/ja-jp/azure/cosmos-db/how-to-setup-rbac
5. `make deploy-azure`でContainer Appsにデプロイ
6. (オプション)Application Insightsを作成
7. (オプション)Application Insightsなどの監視/ログからアラートを設定  
  cf. https://yotiky.hatenablog.com/entry/azure_exceptionsalert
