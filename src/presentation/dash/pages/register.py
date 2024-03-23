import dash
from dash import Input, Output, State, dcc, html
from dash._callback import NoUpdate
from dash.development.base_component import Component
from src.domain.message.message import Message
from src.presentation.dash.app import app
from src.presentation.init import get_message_repository
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
def update_output(n_clicks: int, user_input: str) -> Component | NoUpdate:
    if n_clicks:
        message_repository = get_message_repository()
        usecase = RegisterUsecase(message_repository)
        result = usecase.execute(Message(user_input))
        return html.Div(result)
    return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
