from typing import Annotated

from fastapi import APIRouter, Depends
from injector import Injector, inject

from src.presentation.fastapi.controller.get_injector import get_injector
from src.presentation.fastapi.view_model.error_view_model import ErrorResponse
from src.usecase.error import ErrorUsecase

router = APIRouter()


class ErrorController:
    @inject
    def __init__(self, error_usecase: ErrorUsecase):
        self._error_usecase = error_usecase

    def execute(self) -> ErrorResponse:
        result = self._error_usecase.execute()
        return ErrorResponse(description=result)


@router.get("/error")
def get_error(injector: Annotated[Injector, Depends(get_injector)]) -> ErrorResponse:
    controller = injector.get(ErrorController)
    return controller.execute()
