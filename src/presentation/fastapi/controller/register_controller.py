from fastapi import APIRouter
from injector import inject

from src.di import injector
from src.presentation.fastapi.view_model.register_view_model import (
    RegisterRequest,
    RegisterResponse,
)
from src.usecase.register import RegisterUsecase

router = APIRouter()


class RegisterController:
    @inject
    def __init__(self, register_usecase: RegisterUsecase):
        self._register_usecase = register_usecase

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        result = self._register_usecase.execute(request.to_message())
        return RegisterResponse(text=result)


@router.post("/messages")
def register(request: RegisterRequest) -> RegisterResponse:
    controller = injector.get(RegisterController)
    return controller.execute(request)
