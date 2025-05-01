"""DIコンテナのモジュールを提供する"""

from typing import Any, Optional

from injector import Module, provider, singleton

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


class CommonModule(Module):
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


class LocalModule(CommonModule):
    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    # @singleton  # sqlite3は異なるスレッドからのアクセスができない
    def provide_message_repository(self) -> IMessageRepository:
        return SQLiteMessageRepository(BASE_DIR / "db" / "db.sqlite3")


class TestModule(CommonModule):
    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        # :memory: はスレッド間で共有できずエラーになることがある
        return SQLiteMessageRepository(BASE_DIR / "db" / "test.sqlite3")


class GCPModule(CommonModule):
    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME_HISTORIES
        )


class AWSModule(CommonModule):
    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AWSMessageRepository(AWS_DYNAMODB_TABLE_NAME_HISTORIES)


class AzureModule(CommonModule):
    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AzureMessageRepository(
            AZURE_COSMOS_ENDPOINT,
            AZURE_COSMOS_DATABASE_NAME,
            AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
        )


def get_di_module(
    cloud: Optional[RunEnv] = None,
) -> LocalModule | GCPModule | AWSModule | AzureModule:
    if cloud is None:
        cloud = RUN_ENV

    logger.info(f"DI module: {cloud}")
    match cloud:
        case RunEnv.LOCAL | RunEnv.GITHUB_ACTIONS:  # CI環境もローカルと同じ扱いにする
            return LocalModule()
        case RunEnv.GCP:
            return GCPModule()
        case RunEnv.AWS:
            return AWSModule()
        case RunEnv.AZURE:
            return AzureModule()
        case _:
            raise ValueError("Invalid cloud type")
