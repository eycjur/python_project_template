include .env

.DEFAULT_GOAL := help


## メタ的なコマンド
# デフォルトコマンド(test lint)
.PHONY: all
all: test lint


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
# dockerのサーバーの起動
.PHONY: deploy
deploy:
	gcloud builds submit \
		--region $(REGION) \
		--tag gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
		--project $(PROJECT_ID) \
		.

	gcloud run deploy $(CONTAINER_NAME) \
		--image gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
		--region $(REGION) \
		--port $(APP_PORT) \
		--set-env-vars=$(shell \
			awk 1 .env | \
			grep -vE '^\s*($$|#)' | \
			tr '\n' ',' | \
			sed 's/,$$//' \
		) \
		--cpu 1 \
		--memory 1Gi \
		--platform managed \
		--service-account $(SERVICE_ACCOUNT) \
		--project $(PROJECT_ID)


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
