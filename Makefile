include .env

.DEFAULT_GOAL := help


## python関連のコマンド
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
	ruff --fix .
	ruff format .

.PHONY: mypy
mypy:
	mypy --config-file=pyproject.toml .


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
ENV_JSON := {$(shell awk 1 .env | grep -vE '^\s*($$|\#)' | sed -E 's/^([^=]+)="{0,1}([^"]*)"{0,1}$$/"\1":"\2"/g' | tr '\n' ',' | sed 's/,$$//')}

.PHONY: build-aws
build-aws:
	docker buildx build \
		--platform linux/amd64 \
		--tag ${ECR_URL}/$(CONTAINER_NAME):latest \
		--push \
		.

# AWSへのデプロイ（App Runner、初回実行時）
.PHONY: deploy-aws-init
deploy-aws-init:
	aws ecr get-login-password --region $(AWS_REGION) | \
		docker login --username AWS --password-stdin ${ECR_URL}
	aws ecr create-repository \
		--repository-name $(CONTAINER_NAME) \
		--image-scanning-configuration scanOnPush=true \
		--region $(AWS_REGION) || true
	@make --no-print-directory build-aws
	aws apprunner create-service \
		--service-name $(CONTAINER_NAME) \
		--source-configuration '{ \
				"ImageRepository": { \
					"ImageIdentifier": "${ECR_URL}/$(CONTAINER_NAME):latest", \
					"ImageConfiguration": {"RuntimeEnvironmentVariables": $(ENV_JSON), "Port": "$(CONTAINER_PORT)"}, \
					"ImageRepositoryType": "ECR" \
				}, \
				"AuthenticationConfiguration": { \
					"AccessRoleArn": "arn:aws:iam::$(AWS_ACCOUNT_ID):role/service-role/AppRunnerECRAccessRole" \
				}, \
				"AutoDeploymentsEnabled": true \
			}' \
		--instance-configuration '{ \
				"Cpu":"1024", \
				"Memory":"2048", \
				"InstanceRoleArn": "$(AWS_APPRUNNER_INSTANCE_ROLE_ARN)"\
			}' \
		--region "$(AWS_REGION)"

# AWSへのデプロイ（App Runner、2回目以降）
.PHONY: deploy-aws
deploy-aws:
	@make --no-print-directory build-aws
	aws apprunner update-service \
		--service-arn "$(AWS_APP_RUNNER_SERVICE_ARN)" \
		--source-configuration '{ \
				"ImageRepository": {\
					"ImageIdentifier": "${ECR_URL}/$(CONTAINER_NAME):latest", \
					"ImageConfiguration": {"RuntimeEnvironmentVariables": $(ENV_JSON)}, \
					"ImageRepositoryType": "ECR" \
				} \
			}'

# # AWSへのデプロイ（ECS、初回実行時）
# .PHONY: deploy-aws-init
# deploy-aws-init:
# 	aws ecr get-login-password --region $(AWS_REGION) | \
# 		docker login --username AWS --password-stdin ${ECR_URL}
# 	docker context create ecs ecs-context
# 	aws ecr create-repository \
# 		--repository-name $(CONTAINER_NAME) \
# 		--image-scanning-configuration scanOnPush=true \
# 		--region $(AWS_REGION)

# 	@make --no-print-directory deploy-aws

# # AWSへのデプロイ（ECS、2回目以降）
# .PHONY: deploy-aws
# deploy-aws:
# 	@make --no-print-directory build-aws
# 	$(eval current_context := $(shell docker context ls | grep "\*" | cut -d " " -f 1))
# 	docker context use ecs-context
# 	docker compose -f docker-compose.aws.yml up
# 	docker context use $(current_context)

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


define PRINT_HELP_PYSCRIPT
import sys, re
command_pattern = re.compile(r"^[a-zA-Z0-9\-_]+:")
lines = [line.rstrip() for line in sys.stdin if not line.startswith(".PHONY")]

for previous_line, current_line in zip(lines[:-1], lines[1:]):
	if command_pattern.search(current_line) and previous_line.startswith("# "):
		# #から始まるコメント行があれば、コマンドとコメントを表示
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
