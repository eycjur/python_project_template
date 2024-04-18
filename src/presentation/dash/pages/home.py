from injector import Injector

from dash.development.base_component import Component
from src.di import get_di_module
from src.presentation.dash.component.history import HistoryComponent
from src.usecase.history import HistoryUsecase


def layout() -> Component:
    injector = Injector([get_di_module()])
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return HistoryComponent(messages)
