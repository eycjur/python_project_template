"""
Note:
    コマンド例
    curl http://localhost:${CONTAINER_PORT}/history
    curl -X POST -H "Content-Type: application/json" -d '{"text":"hello"}' http://localhost:${CONTAINER_PORT}/register
    curl http://localhost:${CONTAINER_PORT}/error

"""

from typing import Any

from pydantic import BaseModel

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.domain.message.message import Message
from src.logger.logging import DefaultLogger
from src.presentation.init import get_message_repository
from src.settings import CONTAINER_PORT
from src.usecase.error import ErrorUsecase
from src.usecase.history import HistoryUsecase
from src.usecase.register import RegisterUsecase

logger = DefaultLogger(__name__)
app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Note: 開発用サーバーではエラー時のtraceackがデフォルトで出力されるの重複する
    logger.error(f"Error: {exc}")
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(f"Error: {exc}")
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


class RegisterRequest(BaseModel):
    text: str


class RegisterResponse(BaseModel):
    text: str


class MessageResponse(BaseModel):
    content: str


class HistoryResponse(BaseModel):
    messages: list[MessageResponse]


@app.get("/")
def read_root() -> str:
    return "Hello World"


@app.get("/history")
def history() -> HistoryResponse:
    message_repository = get_message_repository()
    messages = HistoryUsecase(message_repository).execute()
    return HistoryResponse(
        messages=[MessageResponse(content=m.content) for m in messages]
    )


@app.post("/register")
def register(request: RegisterRequest) -> RegisterResponse:
    message_repository = get_message_repository()
    usecase = RegisterUsecase(message_repository)
    result = usecase.execute(Message(request.text))
    return RegisterResponse(text=result)


@app.get("/error")
def error() -> dict[str, Any]:
    result = ErrorUsecase().execute()
    return {"detail": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.fastapi.app:app",
        host="0.0.0.0",
        port=CONTAINER_PORT,
        reload=True,
    )
