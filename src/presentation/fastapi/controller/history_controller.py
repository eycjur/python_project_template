from fastapi import APIRouter
from injector import inject

from src.di import injector
from src.presentation.fastapi.view_model.history_view_model import HistoryResponse
from src.usecase.history import HistoryUsecase

router = APIRouter()


class HistoryController:
    @inject
    def __init__(self, history_usecase: HistoryUsecase):
        self._history_usecase = history_usecase

    def execute(self) -> HistoryResponse:
        messages = self._history_usecase.execute()
        return HistoryResponse.from_messages(messages)


@router.get("/messages")
def get_history() -> HistoryResponse:
    controller = injector.get(HistoryController)
    return controller.execute()
