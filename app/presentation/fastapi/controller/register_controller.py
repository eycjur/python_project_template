from typing import Annotated

from fastapi import APIRouter, Depends
from injector import Injector, inject

from app.di import get_injector
from app.presentation.fastapi.view_model.register_view_model import (
    RegisterRequest,
    RegisterResponse,
)
from app.usecase.register import RegisterUsecase

router = APIRouter()


class RegisterController:
    @inject
    def __init__(self, register_usecase: RegisterUsecase):
        self._register_usecase = register_usecase

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        result = self._register_usecase.execute(request.to_message())
        return RegisterResponse(text=result)


@router.post("/messages")
def register(
    request: RegisterRequest, injector: Annotated[Injector, Depends(get_injector)]
) -> RegisterResponse:
    controller = injector.get(RegisterController)
    return controller.execute(request)
