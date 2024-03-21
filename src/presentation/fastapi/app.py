"""
Note:
    コマンド例
    curl -X POST -H "Content-Type: application/json" -d '{"text":"hello"}' http://localhost:${CONTAINER_PORT}/chat

"""

from pydantic import BaseModel

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.loggers.logging import DefaultLogger
from src.settings import CONTAINER_PORT
from src.usecase.sample import func

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


class ChatRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    text: str


@app.get("/")
def read_root() -> str:
    return "Hello World"


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(text=func(request.text))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.fastapi.app:app",
        host="0.0.0.0",
        port=CONTAINER_PORT,
        reload=True,
    )
