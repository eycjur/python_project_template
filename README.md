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

Cloud Runへのデプロイを実施します

1. サービスアカウントを作成し、そのcredentialファイルをcredentials/credential_gcp.jsonとして保存
2. FirestoreのDBとCollectionを作成
3. `make deploy-gcp`でCloud Runにデプロイ
4. (オプション)Cloud Monitoringのアラートから通知チャンネルを作成
5. (オプション)Cloud Loggingからアラートを設定

### AWS

App Runnerへのデプロイを実施します

1. credentialsをcredentials/credentials_awsとして保存  
  ユーザーアカウントを利用する場合は`cp ~/.aws/credentials credentials/credentials_aws`としてください
2. `make deploy-aws-infra`で、App Runnerに必要なリソースを作成・更新
3. `make deploy-aws`でApp Runnerにデプロイ

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
