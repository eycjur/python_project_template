# [readme]python_project_template

## use
python_project_templateを全て置換
`make install`で環境を構築

## docs
[https://eycjur.github.io/python_project_template/](https://eycjur.github.io/python_project_template/)

## 参考文献
- [python-project-template](https://github.com/rochacbruno/python-project-template)

# 各種ツール使い方

## pyenv
python自体のバージョン管理ツール

### インストール
```bash
brew install pyenv
echo '
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
' >> ~/.zshrc
source ~/.zshrc
```

### pythonのインストール
```bash
# インストールできるバージョンの一覧
pyenv install --list
pyenv install 3.10.1
pyenv global 3.10.1
# インストールされているバージョンの確認
pyenv versions
python -V
```

## poetry
pythonのパッケージ管理ツール

### インストール
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# コンフィグ
poetry config virtualenvs.in-project true
poetry config --list
```

### プロジェクト作成
```bash
# 新規プロジェクト
poetry new my_project
# 他のプロジェクトを参照
poetry install
poetry install -E <extra-name>
```

### パッケージの追加
```bash
poetry add <package>
poetry add <package>==<version>
poetry add <package> --dev

# 環境に依存するパッケージを入れる
poetry add --optional <package>
# extrasを記載
#     [tool.poetry.extras]
#     <extra-name> = ["<package>"]
# 実際にインストラクターするには次が必要
poetry update
poetry install -extras <extra-name>

# アップデート
poetry update <package>
poetry self update

# 削除
poetry remove <package>
```

### その他
```bash
# インストールされているパッケージ一覧
poetry show

# 仮想環境に入る
poetry shell

# 仮想環境内で各種コマンドの実行
poetry run <command>
```

## pytest
pythonのテストツール

### 実行
```bash
poetry run pytest
make test
# 特定ファイルのみ
poetry run pytest tests/test_<file_name>.py
```

## リンター

- flake8  
pythonのコード規約チェックツール
- black  
pythonのフォーマッター
- isort  
pythonのimportのソートツール
- mypy  
pythonの型チェックツール

### 実行
```bash
# まとめて実行
make lint
make lint target=<target>
# 個別に実行
poetry run <tool> .
make <tool>
# 特定ファイルのみ
poetry run <tool> src/<file_name>.py
```

## jupyter notebook
対話型のpython実行環境

### 実行
vscodeでipynbファイルを開くと実行される

ブラウザで開く場合
```bash
make jupyter
```

### git管理
notebook形式ではdiffが見づらいので、pyファイルをgit管理する
```bash
# notebookとpyファイルを同期
make sync-notebook
# pyからnotebookを作成
poetry run jupytext --to notebook notebook/<file_name>.py
```

## sphinx
pythonのドキュメント作成ツール  
docstringを自動で読み取ってhtml形式に変換する  
手動で作成するファイルはdocs/内に配置

### 実行
```bash
make sphinx
make sphinx-reflesh
```

### 出力
docs/_build/以下にhtmlが出力される

## typer
pythonのCLI作成ツール  
src/cli.pyで利用

### 実行
```bash
make cli target=<command>
poetry run python src <command>
# ヘルプを表示
make cli target=--help
poetry run python src --help
poetry run python src <command> --help
```

## profile
実行時間を計測してボトルネックを探す

### 実行
```bash
poetry run python -m cProfile -o logs/profile.stats src/cli.py <command>
poetry run snakeviz ./logs/profile.stats
```

## TODO
ライセンスファイルの追加  
docker対応  
