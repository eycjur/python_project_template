from injector import Injector

from dash import Input, Output, State, dcc, html
from dash.development.base_component import Component
from src.di import get_di_module
from src.domain.message.message import Message
from src.presentation.dash.app import app
from src.usecase.register import RegisterUsecase


def layout() -> Component:
    return html.Div(
        [
            html.H1("投稿ページ"),
            dcc.Input(
                id="user-input", type="text", placeholder="テキストを入力してください"
            ),
            html.Button("Submit", id="submit-button", n_clicks=0),
            html.Div(id="output"),
        ]
    )


@app.callback(
    Output("output", "children"),
    Input("submit-button", "n_clicks"),
    State("user-input", "value"),
    prevent_initial_call=True,
)
def update_output(_: int, user_input: str) -> Component:
    """投稿ボタンが押されたときの処理

    Args:
        n_clicks (int): 押された回数
        user_input (str): ユーザーが入力したテキスト

    Returns:
        Component: 表示するコンポーネント
    """
    injector = Injector([get_di_module()])
    register_usecase = injector.get(RegisterUsecase)
    result = register_usecase.execute(Message(user_input))
    return html.Div(result)


if __name__ == "__main__":
    app.run_server(debug=True)
