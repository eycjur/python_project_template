from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class ErrorUsecase:
    def execute(self) -> str:
        try:
            raise Exception("error")
        except Exception as e:
            logger.error(f"Error: {e}")
        return "Error"
