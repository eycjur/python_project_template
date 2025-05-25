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

from app.shared.controller.message_controller import (
    MessageHistoryController,
    RegisterMessageController,
    handle_controller_error,
)
from app.shared.dto.message_dto import RegisterMessageRequest
from app.shared.injector_factory import get_shared_injector
from app.usecase.error import ErrorUsecase

app = typer.Typer()
injector = get_shared_injector()


@app.command()
def hello() -> None:
    """Hello worldを表示する"""
    typer.echo("hello")


@app.command()
def register(
    text: str = typer.Option("デフォルト", "-t", "--text", help="登録するテキスト"),
) -> None:
    """メッセージを登録する
    
    Args:
        text: 登録するテキスト
    """
    try:
        # 共通DTOを作成
        dto_request = RegisterMessageRequest(text=text)
        
        # 共通コントローラーを使用
        controller = injector.get(RegisterMessageController)
        result = controller.execute(dto_request)
        
        typer.echo(result.message)
        
    except ValueError as e:
        # バリデーションエラー
        error_response = handle_controller_error(e)
        typer.echo(f"エラー: {error_response.error_message}", err=True)
        raise typer.Exit(1)
        
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        typer.echo(f"内部エラー: {error_response.error_message}", err=True)
        raise typer.Exit(1)


@app.command()
def history() -> None:
    """メッセージ履歴を表示する"""
    try:
        # 共通コントローラーを使用
        controller = injector.get(MessageHistoryController)
        result = controller.execute(None)
        
        if result.count == 0:
            typer.echo("メッセージが登録されていません")
        else:
            for msg in result.messages:
                typer.echo(f"[{msg['id']}] {msg['content']}")
                
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        typer.echo(f"エラー: {error_response.error_message}", err=True)
        raise typer.Exit(1)


@app.command()
def error() -> None:
    """エラーを発生させる（テスト用）"""
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    typer.echo(result)


if __name__ == "__main__":
    app()
