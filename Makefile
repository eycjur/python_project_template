# 環境構築の際や後処理を記述

target := .

## メタ的なコマンド
# デフォルトコマンド(test sync_notebook lint)
all: test sync-notebook lint

# ターゲットは関数名みたいな感じで使ってます
.PHONY: list
# すべてのターゲット名を取得
list :  # スペースを空けるとhelpに表示しない
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"

# ヘルプを表示
help:
	@cat $(MAKEFILE_LIST) | python -u -c 'import sys, re; from itertools import tee,chain; rx = re.compile(r"^[a-zA-Z0-9\-_]+:"); xs, ys = tee(sys.stdin); [print(f"""\t{line.split(":")[0]:20s}\t{prev.lstrip("# ").rstrip()}""") if rx.search(line) and prev.startswith("#") else print(f"""\n{prev.lstrip("## ").rstrip()}""") if prev.startswith("##") else "" for prev, line in zip(chain([""], xs), ys)]'

# まとめたもの(lint test sync_notebook sphinx-reflesh)
full: lint test sync-notebook sphinx-reflesh


## 環境構築関連
# 1から環境構築
install:
	poetry install

## python関連のコマンド
# jupyterの起動
lab:
	poetry run jupyter lab
jupyter:
	@make lab

# notebookとpythonスクリプトを同期
sync-notebook:
	poetry run jupytext --sync notebook/*.ipynb

# テストコードの実行
test:
	poetry run pytest

# リンター
lint:
	@make --no-print-directory black
	@make --no-print-directory isort
	@make --no-print-directory flake8
	@make --no-print-directory mypy
mypy:
	poetry run python -m mypy $(target)
black:
	poetry run black $(target)
flake8:
	poetry run flake8 $(target)
isort:
	poetry run isort $(target)

# sphinx（ドキュメント自動作成ツール）関係
sphinx:
	poetry run sphinx-apidoc -f -o ./docs/source ./src
	poetry run sphinx-build -b html ./docs ./docs/_build
sphinx-reflesh:
	rm -rf docs/_build/* docs/source/*.rst
	@make --no-print-directory sphinx

# プロファイリング
profile:
	poetry run python -m cProfile -o logs/profile.stats src/cli.py command
	poetry run snakeviz ./logs/profile.stats

## 実行コマンド
# cli.pyの実行
cli:
	poetry run python src $(target)

## dockerコマンド
# 確認
images:
	docker compose images
ps:
	docker compose ps -a
volume:
	docker volume ls
logs:
	docker compose logs

# 実行
build:
	docker compose build --no-cache --force-rm
up:
	docker compose up -d --build
app:
	docker compose exec app zsh
root:
	docker compose exec -u root app zsh
create-project:
	@make build
	@make up
	@make app
stop:
	docker compose stop
down:
	docker compose down --remove-orphans
restart:
	@make down
	@make up
	@make app
destroy:
	docker compose down --rim all --volumes --remove-orphans
destroy-volumes:
	docker compose down --volumes --remove-orphans
