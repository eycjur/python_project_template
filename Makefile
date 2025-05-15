# タスクランナー用のMakefile
#
# Example:
#	ヘルプ
#
#	$ make

include .env

.DEFAULT_GOAL := help
SHELL := /bin/bash


## Project関連のコマンド
# プロジェクトのミニマイズ
.PHONY: minimize
minimize:
	rm -rf docs/
	rm -rf infra/ Dockerfile.lambda .tflint.hcl cloudbuild.yaml
	rm -rf credentials/
	rm -rf .github/
	rm -rf db/
	rm -rf app/domain app/infrastructure app/usecase
	rm -rf \
		app/logger/logger_config_aws.yaml \
		app/logger/logger_config_azure.yaml \
		app/logger/logger_config_gcp.yaml \
		app/logger/formatter.py
	rm -rf app/di.py
	rm -rf tests/domain
	rm -rf .editorconfig .gcloudignore LICENSE


## Pre-commit関連のコマンド
# pre-commitの実行（全てのファイル）
.PHONY: pre-commit-run-all
pre-commit-run-all:
	pre-commit run --all-files


## Python関連のコマンド
# テストコードの実行
.PHONY: test
test:
	pytest -sv

# リンター
.PHONY: lint
lint:
	@make --no-print-directory ruff
	@make --no-print-directory mypy

.PHONY: ruff
ruff:
	ruff check --fix .
	ruff format .

.PHONY: mypy
mypy:
	mypy --config-file=pyproject.toml .

## Terraform関連のコマンド
# terraformのフォーマット
.PHONY: terraform-fmt
terraform-fmt:
	terraform fmt -recursive

.PHONY: tflint
tflint:
	tflint --recursive --config=$(pwd)/.tflint.hcl

## デプロイ
# GCPのインフラ作成
.PHONY: create-infra-gcp
create-infra-gcp:
	terraform -chdir=infra/gcp init
	terraform -chdir=infra/gcp apply --parallelism=30

# GCPへのデプロイ
.PHONY: deploy-gcp
deploy-gcp:
	gcloud secrets versions add $(GCP_SECRET_MANAGER_SECRET_ID) --data-file=".env"
	# キャッシュを有効にする
	gcloud config set builds/use_kaniko True
	gcloud builds submit \
		--region $(GCP_REGION_CLOUD_BUILD) \
		--project $(GCP_PROJECT_ID) \
		--config cloudbuild.yaml \
		--substitutions=_LOCATION="$(GCP_REGION)",_IMAGE="$(CONTAINER_NAME)" \
		.
	gcloud run deploy $(CONTAINER_NAME) \
		--image $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(CONTAINER_NAME)/$(CONTAINER_NAME) \
		--region $(GCP_REGION) \
		--port $(CONTAINER_PORT) \
		--set-env-vars=CONTAINER_PORT=$(CONTAINER_PORT) \
		--platform managed \
		--service-account $(GCP_SERVICE_ACCOUNT) \
		--project $(GCP_PROJECT_ID)
		# 以下のパラメーターはterraformで設定する
		# --cpu 1 \
		# --memory 1Gi \
		# --ingress internal-and-cloud-load-balancing \

# GCPのインフラ削除
.PHONY: destroy-gcp
destroy-gcp:
	-terraform -chdir=infra/gcp destroy --parallelism=30
	# 保護されたDBを削除
	gcloud alpha firestore databases update --database='$(GCP_FIRESTORE_DB_NAME)' --no-delete-protection
	gcloud alpha firestore databases delete --database='$(GCP_FIRESTORE_DB_NAME)'


ECR_URL = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

# AWSのインフラ作成(AppRunner)
.PHONY: create-infra-aws-apprunner
create-infra-aws-apprunner:
	terraform -chdir=infra/aws_apprunner init
	terraform -chdir=infra/aws_apprunner apply --parallelism=30

# AWSへのデプロイ(AppRunner)
.PHONY: deploy-aws-apprunner
deploy-aws-apprunner:
	# 改行を含む文字列をシークレットマネージャーに登録するために、\\nに置き換える
	aws secretsmanager put-secret-value \
		--secret-id $(AWS_SECRET_MANAGER_SECRET_NAME) \
		--secret-string "$(shell cat .env | sed 's/"/\\"/g' | sed -e ':L' -e 'N' -e '$$!bL' -e 's/\n/\\n/g')"
	aws ecr get-login-password --region $(AWS_REGION) | \
		docker login --username AWS --password-stdin ${ECR_URL}
	docker buildx build \
		--platform linux/amd64 \
		--tag ${ECR_URL}/$(CONTAINER_NAME):latest \
		--push \
		.

# AWSのインフラ削除(AppRunner)
.PHONY: destroy-aws-apprunner
destroy-aws-apprunner:
	-terraform -chdir=infra/aws_apprunner destroy --parallelism=30
	-aws ecr delete-repository --repository-name $(CONTAINER_NAME) --force
	-aws secretsmanager delete-secret --secret-id $(AWS_SECRET_MANAGER_SECRET_NAME) --force-delete-without-recovery

# AWSのインフラ作成(Lambda)
.PHONY: create-infra-aws-lambda
create-infra-aws-lambda:
	terraform -chdir=infra/aws_lambda init
	terraform -chdir=infra/aws_lambda apply --parallelism=30

# AWSへのデプロイ(Lambda)
.PHONY: deploy-aws-lambda
deploy-aws-lambda:
	# 改行を含む文字列をシークレットマネージャーに登録するために、\\nに置き換える
	aws secretsmanager put-secret-value \
		--secret-id $(AWS_SECRET_MANAGER_SECRET_NAME) \
		--secret-string "$(shell cat .env | sed 's/"/\\"/g' | sed -e ':L' -e 'N' -e '$$!bL' -e 's/\n/\\n/g')"
	aws ecr get-login-password --region $(AWS_REGION) | \
		docker login --username AWS --password-stdin ${ECR_URL}
	docker buildx build \
		--platform linux/amd64 \
		--tag $(CONTAINER_NAME):latest \
		--provenance=false \
		.
	docker buildx build \
		--build-arg BASE_IMAGE=$(CONTAINER_NAME) \
		--platform linux/amd64 \
		--tag ${ECR_URL}/$(CONTAINER_NAME):latest \
		--push \
		--provenance=false \
		--file Dockerfile.lambda \
		.
	aws lambda update-function-code \
		--function-name $(CONTAINER_NAME) \
		--image-uri ${ECR_URL}/$(CONTAINER_NAME):latest
	# ローカルのイメージを参照できない場合は、以下のコマンドを実行する
	# docker context use default

# AWSのインフラ削除(Lambda)
.PHONY: destroy-aws-lambda
destroy-aws-lambda:
	-terraform -chdir=infra/aws_lambda destroy --parallelism=30
	-aws ecr delete-repository --repository-name $(CONTAINER_NAME) --force
	-aws secretsmanager delete-secret --secret-id $(AWS_SECRET_MANAGER_SECRET_NAME) --force-delete-without-recovery

# Azureへのデプロイ
.PHONY: deploy-azure
deploy-azure:
	az containerapp compose create \
		--environment containerapps-environment-$(CONTAINER_NAME) \
		--resource-group $(AZURE_RESOURCE_GROUP) \
		--location $(AZURE_LOCATION)
	az containerapp ingress update \
		--name app \
		--resource-group $(AZURE_RESOURCE_GROUP) \
		--target-port $(CONTAINER_PORT) \
		--type external

## dockerの実行コマンド
# コンテナのビルド・起動
.PHONY: up
up:
	docker compose up --build

# コンテナのビルド・起動（キャッシュを使わない）
.PHONY: up-no-cache
up-no-cache:
	docker compose build --no-cache
	docker compose up

# コンテナ内のシェル実行
.PHONY: exec
exec:
	docker compose exec app bash

# コンテナを停止して削除
.PHONY: down
down:
	docker compose down --remove-orphans

# コンテナを再起動
.PHONY: restart
restart:
	@make --no-print-directory down
	@make --no-print-directory up

# コンテナを停止して一括削除
.PHONY: destroy
destroy:
	docker compose down --rmi all --volumes --remove-orphans


# ヘルプを表示する用のスクリプト
define PRINT_HELP_PYSCRIPT
import sys, re
command_pattern = re.compile(r"^[a-zA-Z0-9\-_]+:")
lines = [line.rstrip() for line in sys.stdin if not line.startswith(".PHONY")]

for previous_line, current_line in zip(lines[:-1], lines[1:]):
	if command_pattern.match(current_line) and previous_line.startswith("# "):
		# コマンド行かつ、前の行が#から始まるコメント行であれば、コマンドとコメントを表示
		command = current_line.split(":")[0]
		comment = previous_line.lstrip("# ")
		print(f"{command:20s}\t{comment}")
	elif previous_line.startswith("## "):
		# ##から始まるコメント行があれば、緑字でセクションのタイトルを表示
		section_title = previous_line.lstrip("## ")
		print(f"\n\033[92m{section_title}\033[0m")
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
