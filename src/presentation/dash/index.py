import dash_bootstrap_components as dbc

from dash import Input, Output, dcc, html
from dash.development.base_component import Component
from src.presentation.dash.app import app
from src.presentation.dash.pages import error, home, register
from src.settings import CONTAINER_PORT


def layout() -> Component:
    navbar = dbc.NavbarSimple(
        brand="Home",
        brand_href="/",
        color="dark",
        dark=True,
        className="pb-3 z-3",
    )
    sidebar = html.Div(
        [
            html.H2("Sidebar", className="display-4"),
            html.Hr(),
            html.P("A simple sidebar layout with navigation links", className="lead"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("投稿", href="/register", active="exact"),
                    dbc.NavLink("エラー", href="/error", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
    )
    main = dbc.Container(id="page-content")

    return html.Div(
        [
            dcc.Location(id="url"),
            navbar,
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(sidebar, width=3, className="bg-light pt-3"),
                            dbc.Col(main, width=9, className="pt-3"),
                        ],
                        style={"height": "100vh"},
                    )
                ],
                fluid=True,
            ),
        ]
    )


server = app.server
app.layout = layout


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_content(pathname: str) -> Component:
    """URLに応じてコンテンツを表示する

    Args:
        pathname (str): URLのパス

    Returns:
        Component: 表示するコンポーネント
    """
    page_name = app.strip_relative_path(pathname)
    if not page_name or page_name == "home":
        return home.layout()
    elif page_name == "register":
        return register.layout()
    elif page_name == "error":
        return error.layout()
    return html.H1("404 Not Found")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=CONTAINER_PORT)  # nosec
