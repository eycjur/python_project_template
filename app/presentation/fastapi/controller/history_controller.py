from typing import Annotated

from fastapi import APIRouter, Depends
from injector import Injector, inject

from app.di import get_injector
from app.presentation.fastapi.view_model.history_view_model import HistoryResponse
from app.usecase.history import HistoryUsecase

router = APIRouter()


class HistoryController:
    @inject
    def __init__(self, history_usecase: HistoryUsecase):
        self._history_usecase = history_usecase

    def execute(self) -> HistoryResponse:
        messages = self._history_usecase.execute()
        return HistoryResponse.from_messages(messages)


@router.get("/messages")
def get_history(
    injector: Annotated[Injector, Depends(get_injector)],
) -> HistoryResponse:
    controller = injector.get(HistoryController)
    return controller.execute()
