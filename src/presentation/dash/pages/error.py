from dash import html
from dash.development.base_component import Component

from src.di import injector
from src.usecase.error import ErrorUsecase


def layout() -> Component:
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return html.P(result)
