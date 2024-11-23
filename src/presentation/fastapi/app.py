"""
Note:
    コマンド例
    curl http://localhost:${CONTAINER_PORT}/history
    curl -X POST -H "Content-Type: application/json" -d '{"text":"hello"}' http://localhost:${CONTAINER_PORT}/register
    curl http://localhost:${CONTAINER_PORT}/error

"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.fastapi.controller.error_controller import router as error_router
from src.presentation.fastapi.controller.history_controller import (
    router as history_router,
)
from src.presentation.fastapi.controller.register_controller import (
    router as register_router,
)
from src.presentation.fastapi.exception_handlers import (
    exception_handler,
    validation_exception_handler,
)
from src.settings import CONTAINER_PORT


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    @app.get("/")
    async def health_check() -> dict[str, str]:
        return {"message": "success"}

    app.include_router(register_router)
    app.include_router(history_router)
    app.include_router(error_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.fastapi.app:app",
        host="0.0.0.0",  # nosec  # noqa: S104
        port=CONTAINER_PORT,
        reload=True,
    )
