from injector import inject

from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class ErrorUsecase:
    @inject
    def __init__(self) -> None:
        pass

    def execute(self) -> str:
        try:
            raise Exception("error")
        except Exception as e:
            logger.error(f"Error: {e}")
        return "Error"
