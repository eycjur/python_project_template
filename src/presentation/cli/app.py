"""

Example:
    ヘルプ

    >>> `python -m src.presentation.cli.app --help`

    サブコマンドのヘルプ

    >>> `python -m src.presentation.cli.app [command] --help`

Attention:
    _は-で実行する
"""

import typer

from src.di import injector
from src.domain.message.message import Message
from src.usecase.error import ErrorUsecase
from src.usecase.history import HistoryUsecase
from src.usecase.register import RegisterUsecase

app = typer.Typer()


@app.command()
def hello() -> None:
    typer.echo("hello")


@app.command()
def register(
    text: str = typer.Option("デフォルト", "-t", "--text", help="登録するテキスト"),
) -> None:
    register_usecase = injector.get(RegisterUsecase)
    message = Message(content=text)
    register_usecase.execute(message)
    typer.echo(f"登録しました: {text}")


@app.command()
def history() -> None:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    for m in messages:
        typer.echo(m.content)


@app.command()
def error() -> None:
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    typer.echo(result)


if __name__ == "__main__":
    app()
