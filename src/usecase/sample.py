from src.loggers.logging import DefaultLogger


logger = DefaultLogger(__name__)

def func(user_input: str) -> str:
    logger.info(f"User input: {user_input}")
    return f"あなたの入力は{user_input}です"
