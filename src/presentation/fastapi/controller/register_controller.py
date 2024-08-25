from fastapi import APIRouter
from injector import inject
from pydantic import BaseModel

from src.di import injector
from src.domain.message.message import Message
from src.usecase.register import RegisterUsecase

router = APIRouter()


class RegisterRequest(BaseModel):
    text: str


class RegisterResponse(BaseModel):
    text: str


class RegisterController:
    @inject
    def __init__(self, register_usecase: RegisterUsecase):
        self._register_usecase = register_usecase

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        result = self._register_usecase.execute(Message(request.text))
        return RegisterResponse(text=result)


@router.post("/register")
def register(request: RegisterRequest) -> RegisterResponse:
    controller = injector.get(RegisterController)
    return controller.execute(request)
