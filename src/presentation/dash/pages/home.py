from dash.development.base_component import Component

from src.presentation.dash.component.history import HistoryComponent
from src.presentation.dash.injector import injector
from src.usecase.history import HistoryUsecase


def layout() -> Component:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return HistoryComponent(messages)
