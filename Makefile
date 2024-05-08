# タスクランナー用のMakefile
#
# Example:
#	ヘルプ
#
#	$ make

include .env

.DEFAULT_GOAL := help


## Project関連のコマンド
# プロジェクトのミニマイズ
.PHONY: minimize
minimize:
	rm -rf infra/
	rm -rf credentials/
	rm -rf .github/
	rm -rf db/
	rm -rf src/domain src/infrastructure src/usecase
	rm -rf \
		src/logger/logger_config_aws.yaml \
		src/logger/logger_config_azure.yaml \
		src/logger/logger_config_gcp.yaml \
		src/logger/formatter.py
	rm -rf src/di.py
	rm -rf tests/domain
	rm -rf .editorconfig .gcloudignore LICENSE


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
.PHONY: fmt-terraform
fmt-terraform:
	terraform fmt -recursive

## デプロイ
# GCPへのデプロイ
.PHONY: deploy-gcp
deploy-gcp:
	gcloud builds submit \
		--region $(GCP_REGION_CLOUD_BUILD) \
		--tag gcr.io/$(GCP_PROJECT_ID)/$(CONTAINER_NAME) \
		--project $(GCP_PROJECT_ID) \
		.

	gcloud run deploy $(CONTAINER_NAME) \
		--image gcr.io/$(GCP_PROJECT_ID)/$(CONTAINER_NAME) \
		--region $(GCP_REGION) \
		--port $(CONTAINER_PORT) \
		--set-env-vars=$(shell \
			awk 1 .env | \
			grep -vE '^\s*($$|#)' | \
			tr '\n' ',' | \
			sed 's/,$$//' \
		) \
		--cpu 1 \
		--memory 1Gi \
		--platform managed \
		--service-account $(GCP_SERVICE_ACCOUNT) \
		--project $(GCP_PROJECT_ID)

ECR_URL = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

# AWSへのフルデプロイ（環境変数の更新含む）
.PHONY: deploy-aws-infra
deploy-aws-infra:
	terraform -chdir=infra/aws init
	terraform -chdir=infra/aws apply

# AWSへのデプロイ
.PHONY: deploy-aws
deploy-aws:
	aws ecr get-login-password --region $(AWS_REGION) | \
		docker login --username AWS --password-stdin ${ECR_URL}
	docker buildx build \
		--platform linux/amd64 \
		--tag ${ECR_URL}/$(CONTAINER_NAME):latest \
		--push \
		.

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
