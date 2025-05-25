"""DIコンテナのモジュールと共通のInjectorインスタンスを提供する"""

from abc import ABC, abstractmethod
from typing import Any

from injector import Injector, Module, provider, singleton

from app.domain.message.message_repository import IMessageRepository
from app.infrastructure.repository.message.aws_message_repository import (
    AWSMessageRepository,
)
from app.infrastructure.repository.message.azure_message_repository import (
    AzureMessageRepository,
)
from app.infrastructure.repository.message.gcp_message_repository import (
    GCPMessageRepository,
)
from app.infrastructure.repository.message.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from app.logger.logging import DefaultLogger
from app.settings import (
    AWS_DYNAMODB_TABLE_NAME_HISTORIES,
    AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
    AZURE_COSMOS_DATABASE_NAME,
    AZURE_COSMOS_ENDPOINT,
    BASE_DIR,
    GCP_FIRESTORE_COLLECTION_NAME_HISTORIES,
    GCP_FIRESTORE_DB_NAME,
    RUN_ENV,
    RunEnv,
)
from app.usecase.error import ErrorUsecase
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase

logger = DefaultLogger(__name__)
_global_injector: Injector | None = None


class CommonModule(Module, ABC):
    def configure(self, binder: Any) -> None:
        """DIコンテナに登録するクラスを設定する

        Hint:
            binder.bind(interface_B, to=class_B)でinterfaceに対してclassを紐付ける
            この設定を行うことで、interfaceを引数に持つクラスのインスタンスを取得する際に、自動的にclassのインスタンスが注入される

            >>> from injector import inject
            >>> class class_A:
            >>>     @inject
            >>>     def __init__(self, instance_B: interface_B):
            >>>         pass
            >>>
            >>> injector = Injector([CommonModule()])
            >>> instance_A = injector.get(class_A)
        """
        binder.bind(RegisterUsecase, to=RegisterUsecase)
        binder.bind(HistoryUsecase, to=HistoryUsecase)
        binder.bind(ErrorUsecase, to=ErrorUsecase)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @abstractmethod
    def provide_message_repository(self) -> IMessageRepository:
        pass


class LocalModule(CommonModule):
    @provider
    # @singleton  # sqlite3は異なるスレッドからのアクセスができない
    def provide_message_repository(self) -> IMessageRepository:
        return SQLiteMessageRepository(BASE_DIR / "db" / "db.sqlite3")


class TestModule(CommonModule):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return SQLiteMessageRepository(":memory:")


class GCPModule(CommonModule):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME_HISTORIES
        )


class AWSModule(CommonModule):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AWSMessageRepository(AWS_DYNAMODB_TABLE_NAME_HISTORIES)


class AzureModule(CommonModule):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AzureMessageRepository(
            AZURE_COSMOS_ENDPOINT,
            AZURE_COSMOS_DATABASE_NAME,
            AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
        )


def _get_di_module(
    cloud: RunEnv | None = None,
) -> LocalModule | TestModule | GCPModule | AWSModule | AzureModule:
    if cloud is None:
        cloud = RUN_ENV

    logger.info(f"DI module: {cloud}")
    match cloud:
        case RunEnv.LOCAL | RunEnv.GITHUB_ACTIONS:  # CI環境もローカルと同じ扱いにする
            return LocalModule()
        case RunEnv.TEST:
            return TestModule()
        case RunEnv.GCP:
            return GCPModule()
        case RunEnv.AWS:
            return AWSModule()
        case RunEnv.AZURE:
            return AzureModule()
        case _:
            raise ValueError(f"Invalid cloud type {cloud}")


def get_injector(is_test: bool = False) -> Injector:
    """DIコンテナのモジュールを取得する

    Args:
        is_test (bool): テスト環境かどうか。デフォルトはFalse。

    Returns:
        Injector: DIコンテナのインスタンス
    """
    global _global_injector
    if _global_injector is not None:
        return _global_injector

    logger.info("Creating new injector instance")
    if is_test:
        _global_injector = Injector(_get_di_module(RunEnv.TEST))
    else:
        _global_injector = Injector(_get_di_module())
    return _global_injector


def reset_injector() -> None:
    """グローバルなInjectorインスタンスをリセットする (主にテスト用)"""
    global _global_injector
    _global_injector = None
    logger.info("Reset global injector instance")
