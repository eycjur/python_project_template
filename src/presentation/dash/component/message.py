import dash_bootstrap_components as dbc
from dash.html import P

from src.domain.message.message import Message


class MessageComponent(dbc.Card):
    def __init__(self, messages: Message):
        super().__init__([dbc.CardBody([P(messages._content)])])
