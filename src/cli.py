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

from typing import Optional

import typer

from src.add.add import add
from src.config import settings  # noqa

app = typer.Typer()


@app.command()
def hello() -> None:
    """hello"""
    typer.echo("hello")


@app.command()
def sample(
    text: Optional[str] = typer.Option(None, "-t", "--text", help="出力する文字列")
) -> None:
    """メインコマンド"""
    print("text:", text)
    print(settings.cfg.is_debug_mode)
    print(add(3, 5))


typer_click_object = typer.main.get_command(app)


def main() -> None:
    typer_click_object()
