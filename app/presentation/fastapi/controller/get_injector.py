from injector import Injector

from app.di import get_injector as _get_injector


def get_injector() -> Injector:
    return _get_injector()
