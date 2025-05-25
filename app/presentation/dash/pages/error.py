from dash import html
from dash.development.base_component import Component

from app.di import get_injector
from app.usecase.error import ErrorUsecase


def layout() -> Component:
    injector = get_injector()
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return html.P(result)
