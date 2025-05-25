from dash.development.base_component import Component

from app.di import get_injector
from app.presentation.dash.component.history import HistoryComponent
from app.usecase.history import HistoryUsecase


def layout() -> Component:
    injector = get_injector()
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return HistoryComponent(messages)
