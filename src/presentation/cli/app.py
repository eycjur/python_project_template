"""

Example:
    ヘルプ

    >>> `python cli.py --help`

    サブコマンドのヘルプ

    >>> `python cli.py [command] --help`

Attention:
    _は-で実行する
"""

import typer

from src.usecase.sample import func

app = typer.Typer()


@app.command()
def hello() -> None:
    typer.echo("hello")


@app.command()
def sample(
    text: str = typer.Option("デフォルト", "-t", "--text", help="任意の文字列"),
) -> None:
    typer.echo(func(text))


if __name__ == "__main__":
    app()
