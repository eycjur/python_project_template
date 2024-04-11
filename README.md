# Python Project Template
pythonでプロジェクトを作成する際のテンプレートです。

## How to Minimize

各種クラウドでの動作確認等を行うため、最小限+αの構成としています。  
最小限の構成として利用する場合は、以下の手順で不要なファイルを削除してください。

1. credentials/を削除、docker-compose.ymlからcredentialsのマウントを削除
2. infra/を削除
3. .github/を削除
4. src/domain, src/infrastructure, src/usecaseを削除
5. src/presentation/のサブディレクトリの内、不要なフレームワークのディレクトリを削除
6. tests/domainを削除
7. .gcloudignore, docker-compose.aws.yml, LICENSEを削除
8. README.mdを編集
9. クラウド関係の環境変数を.envから削除

## How to Run

1. .env.sampleを元に.envを作成
2. `make up`でDocker Composeを起動
3. http://localhost:<LOCAL_PORT>/ からアプリにアクセス
4. `make down`でDocker Composeを終了  
   終了せずにDev Containerを起動すると、docker-compose.override.ymlの内容が上書きされずデバッグが利用できません。

## How to Develop

1. .env.sampleを元に.envを作成
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

1. サービスアカウントを作成し、そのcredentialファイルをcredentials/credential_gcp.jsonとして保存
2. `make deploy-gcp`でCloud Runにデプロイ

### AWS

App Runnerへのデプロイを実施します

1. credentialsをcredentials/credentials_awsとして保存
2. `make deploy-aws-infra`で、App Runnerに必要なリソースを作成・更新
3. `make deploy-aws`でApp Runnerにデプロイ

> [!NOTE]
> ※makefileでコメントアウトしている部分を有効化することで、ECSにデプロイすることも可能です
> デプロイ後、ECS/クラスター/<CONTAINER_NAME>/タスク/\<id>/パブリックIPアドレスに表示されるアドレスにアクセスしてください

### Azure

Container Appsへのデプロイを実施します

1. Entra IDからアプリを登録し、クライアントシークレットを発行する
2. credentialsをcredentials/credentials_azure、configをconfig_azureとして保存
3. .envのAZURE_CLIENT_ID,AZURE_CLIENT_SECRETに各値を設定
4. CosmosDBへのアクセス権の付与  
    ```shell
    az cosmosdb sql role assignment create \
    --account-name <CosmosDBのアカウント名> \
    --resource-group <リソースグループ名> \
    --scope "/" \
    --principal-id <EntraIDのエンタープライズアプリケーションの該当アプリケーションのオブジェクトID> \
    --role-definition-id <ロールid=00000000-0000-0000-0000-000000000002>
   ```   
    cf. https://learn.microsoft.com/ja-jp/azure/cosmos-db/how-to-setup-rbac
5. `make deploy-azure`でContainer Appsにデプロイ

## TODO

- [ ] ECS実行時のサービスの実行ロールを付与
- [ ] Azureのロールベースのアクセス制御
- [ ] コンテナ内のユーザー設定(UID,GIDを.envに記載する必要がある)

```Dockerfile
# 参考
ARG UID=2000
ARG GID=2000
ARG USER_NAME=dev
ARG GROUP_NAME=dev

RUN groupadd -g $GID $GROUP_NAME \
    && useradd -lm -u $UID -g ${GID} $USER_NAME \
    && usermod -aG sudo $USER_NAME \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ${USER_NAME}
```
