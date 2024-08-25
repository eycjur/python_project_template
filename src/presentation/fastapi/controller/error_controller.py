from fastapi import APIRouter
from injector import inject

from src.di import injector
from src.usecase.error import ErrorUsecase

router = APIRouter()


class ErrorController:
    @inject
    def __init__(self, error_usecase: ErrorUsecase):
        self._error_usecase = error_usecase

    def execute(self) -> dict:
        result = self._error_usecase.execute()
        return {"detail": result}


@router.get("/error")
def get_error() -> dict:
    controller = injector.get(ErrorController)
    return controller.execute()
