"""
Note:
    コマンド例
    curl -X POST -H "Content-Type: application/json" -d '{"text":"hello"}' http://localhost:${APP_PORT}/chat

"""

from pydantic import BaseModel

from fastapi import FastAPI
from src.settings import APP_PORT
from src.usecase.sample import func

app = FastAPI()


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
        "src.presentation.fastapi.app:app", host="0.0.0.0", port=APP_PORT, reload=True
    )
