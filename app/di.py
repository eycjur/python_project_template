"""DIコンテナのモジュールと共通のInjectorインスタンスを提供する"""

from typing import Any, Optional

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
        self._bind_usecases(binder)

    def _bind_usecases(self, binder: Any) -> None:
        """Usecaseクラスをシングルトンとしてバインドする"""
        binder.bind(RegisterUsecase, to=RegisterUsecase, scope=singleton)
        binder.bind(HistoryUsecase, to=HistoryUsecase, scope=singleton)
        binder.bind(ErrorUsecase, to=ErrorUsecase, scope=singleton)


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
    def provide_message_repository(self) -> IMessageRepository:
        # :memory: はスレッド間で共有できずエラーになることがある
        # テスト環境ではsingletonを使わずに毎回新しいインスタンスを作成
        return SQLiteMessageRepository(BASE_DIR / "db" / "test.sqlite3")


class CloudModuleBase(CommonModule):
    """クラウドプロバイダー用の基底クラス"""

    def configure(self, binder: Any) -> None:
        super().configure(binder)
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        """サブクラスで実装する必要がある"""
        raise NotImplementedError("Subclasses must implement this method")


class GCPModule(CloudModuleBase):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME_HISTORIES
        )


class AWSModule(CloudModuleBase):
    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AWSMessageRepository(AWS_DYNAMODB_TABLE_NAME_HISTORIES)


class AzureModule(CloudModuleBase):
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
) -> LocalModule | TestModule | GCPModule | AWSModule | AzureModule:
    """環境に応じたDIモジュールを取得する"""
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
            raise ValueError(f"Invalid cloud type: {cloud}")


_global_injector: Optional[Injector] = None


def get_injector(cloud: Optional[RunEnv] = None) -> Injector:
    """共通のInjectorインスタンスを取得する（シングルトンパターン）"""
    global _global_injector
    
    if _global_injector is None:
        module = get_di_module(cloud)
        _global_injector = Injector(module)
        logger.info("Created new global injector instance")
    
    return _global_injector


def reset_injector() -> None:
    """グローバルなInjectorインスタンスをリセットする（主にテスト用）"""
    global _global_injector
    _global_injector = None
    logger.info("Reset global injector instance")
