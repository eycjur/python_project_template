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

from src.domain.message.message import Message
from src.init import get_message_repository
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
    message_repository = get_message_repository()
    message = Message(content=text)
    RegisterUsecase(message_repository).execute(message)
    typer.echo(f"登録しました: {text}")


@app.command()
def history() -> None:
    message_repository = get_message_repository()
    messages = HistoryUsecase(message_repository).execute()
    for m in messages:
        typer.echo(m.content)


@app.command()
def error() -> None:
    result = ErrorUsecase().execute()
    typer.echo(result)


if __name__ == "__main__":
    app()
