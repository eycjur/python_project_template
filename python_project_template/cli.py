"""各種pythonファイルをコマンドラインから利用するためのCLIツール

See Also:
    - `typer`_

    .. _typer: https://qiita.com/iisaka51/items/18bde4dada0827fbe81e

Example:
    ヘルプ

    >>> `python cli.py --help`

    サブコマンドのヘルプ

    >>> `python cli.py [command] --help`

Attention:
    _は-で実行する
"""

import typer
from add.add import add
from conf.conf import CFG
from utils import settings  # noqa

app = typer.Typer()


@app.command()
def hello() -> None:
    """hello"""
    typer.echo("hello")


@app.command()
def main() -> None:
    """メインコマンド"""
    print(CFG.is_debug_mode)
    print(add(3, 5))


typer_click_object = typer.main.get_command(app)


if __name__ == "__main__":
    typer_click_object()
