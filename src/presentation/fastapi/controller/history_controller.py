from fastapi import APIRouter
from injector import inject
from pydantic import BaseModel

from src.di import injector
from src.usecase.history import HistoryUsecase

router = APIRouter()


class MessageResponse(BaseModel):
    content: str


class HistoryResponse(BaseModel):
    messages: list[MessageResponse]


class HistoryController:
    @inject
    def __init__(self, history_usecase: HistoryUsecase):
        self._history_usecase = history_usecase

    def execute(self) -> HistoryResponse:
        messages = self._history_usecase.execute()
        return HistoryResponse(
            messages=[MessageResponse(content=m._content) for m in messages]
        )


@router.get("/history")
def get_history() -> HistoryResponse:
    controller = injector.get(HistoryController)
    return controller.execute()
