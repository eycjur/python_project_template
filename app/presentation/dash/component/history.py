import dash_bootstrap_components as dbc

from app.domain.message.message import Message
from app.presentation.dash.component.message import MessageComponent


class HistoryComponent(dbc.Container):
    def __init__(self, history: list[Message]):
        super().__init__([MessageComponent(message) for message in history])
