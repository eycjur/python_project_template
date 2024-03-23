# Python Project Template
pythonでプロジェクトを作成する際のテンプレートです。

## How to Run

1. .env.sampleを元に.envを作成、利用するクラウドのクレデンシャルファイルをcredentials/を配置
   1. GCPの場合は、サービスアカウントのcredentialファイルをcredential_gcp.jsonとして保存
   2. AWSの場合は、クレデンシャルファイルをcredential_awsとして保存
2. `make up`でDocker Composeを起動
3. http://localhost:<LOCAL_PORT>/ からアプリにアクセス
4. `make down`でDocker Composeを終了  
   終了せずにDev Containerを起動すると、docker-compose.override.ymlの内容が上書きされずデバッグが利用できません。

## How to Develop

1. .env.sampleを元に.envを作成、利用するクラウドのクレデンシャルファイルをcredentials/を配置
2. pre-commitをインストール(ex. `pip install pre-commit`)
3. `pre-commit install`でpre-commitのhookスクリプトを導入
4. VSCodeでDev Container拡張機能をインストール
5. コマンドパレット(`Ctrl+Shift+P`)から`Remote-Containers: Reopen in Container`を実行
6. (Docker Compose立ち上げ時のみ)拡張機能の依存関係の解決に失敗するので、通知に従ってウィンドウの再読み込みする
7. F5でデバッグ実行が可能
8. http://localhost:<LOCAL_PORT>/ からアプリにアクセス

## How to Deploy

### GCP

Cloud Runへのデプロイを実施します

1. `make deploy-gcp`でCloud Runにデプロイ

### AWS

App Runnerへのデプロイを実施します

1. 初回デプロイ時は、`make deploy-aws-init`でApp Runnerにデプロイ
2. 2回目以降は、`make deploy-aws`でApp Runnerにデプロイ

> [!NOTE]
> ※makefileでコメントアウトしている部分を有効化することで、ECSにデプロイすることも可能です
> デプロイ後、ECS/クラスター/<CONTAINER_NAME>/タスク/\<id>/パブリックIPアドレスに表示されるアドレスにアクセスしてください

### Azure

Container Appsへのデプロイを実施します

1. `make deploy-azure`でContainer Appsにデプロイ

## TODO

- [ ] ECS実行時のサービスの実行ロールを付与
