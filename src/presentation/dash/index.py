import dash_bootstrap_components as dbc

from dash import Input, Output, dcc, html
from dash.development.base_component import Component
from src.presentation.dash.app import app
from src.presentation.dash.pages import home
from src.settings import CONTAINER_PORT


def layout() -> Component:
    navbar = dbc.NavbarSimple(
        brand="Home", brand_href="/", color="dark", dark=True, className="mb-3"
    )
    return html.Div(
        [dcc.Location(id="url"), navbar, dbc.Container(id="page-content", fluid=True)]
    )


server = app.server
app.layout = layout


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_content(pathname: str) -> Component:
    page_name = app.strip_relative_path(pathname)
    if not page_name:
        return home.layout()
    return html.H1("404 Not Found")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=CONTAINER_PORT)
