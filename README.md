[![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Feycjur%2Fpython_project_template%2Fmain%2Fpyproject.toml)](https://github.com/eycjur/python_project_template/blob/main/pyproject.toml)
[![Static Analysis](https://github.com/eycjur/python_project_template/actions/workflows/static_analysis.yml/badge.svg)](https://github.com/eycjur/python_project_template/actions/workflows/static_analysis.yml)
[![Test](https://github.com/eycjur/python_project_template/actions/workflows/test.yml/badge.svg)](https://github.com/eycjur/python_project_template/actions/workflows/test.yml)
[![Container Security](https://github.com/eycjur/python_project_template/actions/workflows/container_security.yml/badge.svg)](https://github.com/eycjur/python_project_template/actions/workflows/container_security.yml)
[![Container Security](https://github.com/eycjur/python_project_template/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/eycjur/python_project_template/actions/workflows/github-code-scanning/codeql)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/eycjur/python_project_template)

# Python Project Template
pythonでプロジェクトを作成する際のテンプレートです。

## About

本リポジトリは、PythonでWebアプリケーションを開発する際のテンプレートです。

サンプルとして、メッセージ管理アプリケーションを実装しています。

### ユースケース図

<img src="docs/usecase/usecase.png" width="320px">

### 機能要件

| 機能 | 詳細 | ユースケース |
| --- | --- | --- |
| メッセージの登録 | メッセージを登録する | メッセージ登録 |
| メッセージの閲覧 | メッセージを閲覧する | メッセージ閲覧 |

#### 画面遷移図

<img src="docs/requirements/screen_transition.png" width="320px">

#### API仕様(FastAPI)

| メソッド | パス | 説明 |
| --- | --- | --- |
| GET | /messages | メッセージ一覧を取得 |
| POST | /messages | メッセージを登録 |

## Features

以下の機能を提供しています。

- UI
    - CLI(typer)
    - API(FastAPI)
    - サーバーサイドレンダリング(Flask)
    - UIフレームワーク(streamlit, dash)
- データベース
    - SQLite
    - Firestore
    - DynamoDB
    - CosmosDB
- クラウド
    - GCP(Cloud Run)
    - AWS(App Runner, Lambda)
    - Azure(Container Apps)
- CI/CD
    - GitHub Actions
- テスト
    - unit test
    - e2e test
- ログ
- モニタリング

## Architecture

Onion Architectureを採用しています。

UIフレームワークによって詳細は異なりますが、FastAPIを利用する場合のアーキテクチャ図を以下に示します。

<img src="docs/architecture/architecture_fastapi.png" width="640px">

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
3. app/presentation/のサブディレクトリのうち、不要なフレームワークのディレクトリを削除
4. .devcontainer/devcontainer.jsonのlaunchの設定のうち、不要なフレームワークの設定を削除
5. README.mdを編集
6. クラウド関係の環境変数を.envとapp/settings.pyから削除

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
2. live-server拡張機能で、app/presentation/fastapi/frontend/index.htmlを開く
3. http://localhost:5500/app/presentation/fastapi/frontend/ からフロントエンドにアクセス

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
