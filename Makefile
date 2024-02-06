include .env

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
	@make --no-print-directory black
	@make --no-print-directory ruff
	@make --no-print-directory mypy

.PHONY: black
black:
	black --config-file=pyproject.toml .

.PHONY: ruff
isort:
	ruff .

.PHONY: mypy
mypy:
	python -m mypy --config-file=pyproject.toml .


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
		--port $(PORT) \
		--set-env-vars=$(shell \
			cat .env | \
			grep -vE '^\s*($$|#)' | \
			tr '\n' ',' | \
			sed 's/,$$//' \
		) \
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
	@make up
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


.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | python3 -u -c 'import sys, re; rx = re.compile(r"^[a-zA-Z0-9\-_]+:"); lines = [line.rstrip() for line in sys.stdin if not line.startswith(".PHONY")]; [print(f"""{line.split(":")[0]:20s}\t{prev.lstrip("# ")}""") if rx.search(line) and prev.startswith("# ") else print(f"""\n\033[92m{prev.lstrip("## ")}\033[0m""") if prev.startswith("## ") else "" for prev, line in zip([""] + lines, lines)]'
