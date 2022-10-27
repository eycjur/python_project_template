include .env
shell_name = zsh
target := .

## メタ的なコマンド
# デフォルトコマンド(test sync_notebook lint)
.PHONY: all
all: test sync-notebook lint

# まとめたもの(lint test sync_notebook sphinx-reflesh)
.PHONY: full
full: lint test sync-notebook sphinx-reflesh

# docker関連のコマンドをまとめたもの（build exec）
.PHONY: docker
docker: build exec


## python関連のコマンド
# jupyterの起動
.PHONY: lab
lab:
	jupyter lab
.PHONY: jupyter
jupyter:
	@make lab

# notebookとpythonスクリプトを同期
.PHONY: sync-notebook
sync-notebook:
	jupytext --sync notebook/*.ipynb

# テストコードの実行
.PHONY: test
test:
	pytest

# リンター
.PHONY: lint
lint:
	@make --no-print-directory black
	@make --no-print-directory isort
	@make --no-print-directory flake8
	@make --no-print-directory mypy
	@make --no-print-directory radon
.PHONY: black
black:
	black $(target)
.PHONY: isort
isort:
	isort $(target)
.PHONY: flake8
flake8:
	flake8 $(target)
.PHONY: mypy
mypy:
	python -m mypy $(target)
.PHONY: radon
radon:
	echo "循環的複雑度"
	radon cc -s -nb $(target)
	echo "保守容易性指数"
	radon mi -s -nb $(target)

# sphinx（ドキュメント自動作成ツール）関係
.PHONY: sphinx
sphinx:
	sphinx-apidoc -f -o ./docs/source ./src
	sphinx-build -b html ./docs ./docs/_build
# キャッシュを削除してsphinxを実行
.PHONY: sphinx-reflesh
sphinx-reflesh:
	rm -rf docs/_build/* docs/source/*.rst
	@make --no-print-directory sphinx
# ドキュメントをブラウザで開く
.PHONY: open-docs
open-docs:
	open -a "Google Chrome" docs/_build/index.html

# プロファイリング
.PHONY: profile
profile:
	python -m cProfile -o logs/profile.stats src/cli.py command
	snakeviz ./logs/profile.stats


## 実行コマンド
# cli.pyの実行
.PHONY: cli
cli:
	python -m src $(target)


## dockerコンテナ内でのコマンド
# サーバーを起動する
.PHONY: server
server:
	python app.py

# デプロイ
.PHONY: deploy
deploy:
	./deploy.sh

# pip freeze
.PHONY: pip-freeze
pip-freeze:
	python -m pip freeze > requirements.txt


## dockerの確認コマンド
# 確認
.PHONY: images
images:
	docker images

# コンテナを一覧表示
.PHONY: ps
ps:
	docker compose ps -a

# volumeを一覧表示
.PHONY: volumes
volumes:
	docker volume ls

# dockerのlogを表示
.PHONY: logs
logs:
	docker compose logs


## dockerの実行コマンド
# ビルド
.PHONY: build
build:
	docker compose build

# コンテナの起動
.PHONY: up
up:
	docker compose up -d --build

# 実行
.PHONY: exec
exec:
	@make up
	docker compose exec app ${shell_name}

# コンテナを停止
.PHONY: stop
stop:
	docker compose stop

# コンテナを停止して削除
.PHONY: down
down:
	docker compose down --remove-orphans

# コンテナを停止して一括削除
.PHONY: destroy
destroy:
	docker compose down --rmi all --volumes --remove-orphans

# dockerの未使用オブジェクトを削除
.PHONY: prune
prune:
	docker system prune -af


.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | python3 -u -c 'import sys, re; rx = re.compile(r"^[a-zA-Z0-9\-_]+:"); lines = [line.rstrip() for line in sys.stdin if not line.startswith(".PHONY")]; [print(f"""{line.split(":")[0]:20s}\t{prev.lstrip("# ")}""") if rx.search(line) and prev.startswith("# ") else print(f"""\n\033[92m{prev.lstrip("## ")}\033[0m""") if prev.startswith("## ") else "" for prev, line in zip([""] + lines, lines)]'
