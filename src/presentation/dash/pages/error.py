from injector import Injector

from dash import html
from dash.development.base_component import Component
from src.di import get_di_module
from src.usecase.error import ErrorUsecase


def layout() -> Component:
    injector = Injector([get_di_module()])
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return html.P(result)
