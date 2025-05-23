from injector import Injector

from app.di import get_di_module


def get_injector() -> Injector:
    return Injector(get_di_module())
