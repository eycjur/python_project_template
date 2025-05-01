from dash.development.base_component import Component

from app.presentation.dash.component.history import HistoryComponent
from app.presentation.dash.injector import injector
from app.usecase.history import HistoryUsecase


def layout() -> Component:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return HistoryComponent(messages)
