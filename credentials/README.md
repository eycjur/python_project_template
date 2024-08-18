# credentials
クラウドのクレデンシャルファイルを格納するディレクトリです。

## ファイル構成

docker-compose.ymlでコンテナ内の/credentialsにマウントされます。  
docker-compose.ymlのenvironmentで指定したパスにクレデンシャルファイルが存在する必要があるので、以下のファイル名で配置してください。

### GCP

サービスアカウントを作成し、Cloud Runの実行およびローカルでの開発ではそのサービスアカウントを使用する

- `credential_gcp.json`: GCPのサービスアカウントのキー

### AWS

App Runnerの実行は、Terraformで作成したロールを使用します。  
ローカルでの開発時は、IAMユーザーを作成し、ローカルでの開発ではそのIAMユーザーのクレデンシャルを使用します

- `credentials_aws`: AWSのクレデンシャルファイル

### Azure

Container Appsでの実行および、ローカルでの開発時は、サービスプリンシパル（アプリを登録から登録）を作成します  
本来はマネージドID（コンテナアプリの画面から、設定>IDで状態をオンにする）を利用する方が良いが、オンにできない

環境変数AZURE_CLIENT_ID,AZURE_CLIENT_SECRETで指定するので、クレデンシャルファイルは不要です。
