from dash import html
from dash.development.base_component import Component
from src.usecase.error import ErrorUsecase


def layout() -> Component:
    result = ErrorUsecase().execute()
    return html.P(result)
