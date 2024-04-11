# credentials
クラウドのクレデンシャルファイルを格納するディレクトリです。

## ファイル構成

docker-compose.ymlでコンテナ内の/credentialsにマウントされます。  
docker-compose.ymlのenvironmentで指定したパスにクレデンシャルファイルが存在する必要があるので、以下のファイル名で配置してください。

### GCP

- `credential_gcp.json`: GCPのサービスアカウントキー

### AWS

- `credentials_aws`: AWSのクレデンシャルファイル

### Azure

環境変数AZURE_CLIENT_ID,AZURE_CLIENT_SECRETで指定するので、クレデンシャルファイルは不要です。
