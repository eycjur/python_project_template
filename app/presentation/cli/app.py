"""

Example:
    ヘルプ

    >>> `python -m app.presentation.cli.app --help`

    サブコマンドのヘルプ

    >>> `python -m app.presentation.cli.app [command] --help`

Attention:
    _は-で実行する
"""

import typer

from app.di import get_injector
from app.domain.message.message import Message
from app.usecase.error import ErrorUsecase
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase

app = typer.Typer()
injector = get_injector()


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
