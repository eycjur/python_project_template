"""DIコンテナのモジュールを提供する"""

from typing import Any, Optional

from injector import Module, provider, singleton

from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.aws_message_repository import (
    AWSMessageRepository,
)
from src.infrastructure.repository.message.azure_message_repository import (
    AzureMessageRepository,
)
from src.infrastructure.repository.message.gcp_message_repository import (
    GCPMessageRepository,
)
from src.infrastructure.repository.message.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from src.settings import (
    AWS_DYNAMODB_TABLE_NAME_HISTORIES,
    AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
    AZURE_COSMOS_DATABASE_NAME,
    AZURE_COSMOS_ENDPOINT,
    BASE_DIR,
    CLOUD,
    GCP_FIRESTORE_COLLECTION_NAME_HISTORIES,
    GCP_FIRESTORE_DB_NAME,
    CloudType,
)


class LocalModule(Module):
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
            >>> injector = Injector([LocalModule()])
            >>> instance_A = injector.get(class_A)
        """
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    def provide_message_repository(self) -> IMessageRepository:
        return SQLiteMessageRepository(BASE_DIR / "db" / "db.sqlite3")


class GCPModule(Module):
    def configure(self, binder: Any) -> None:
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME_HISTORIES
        )


class AWSModule(Module):
    def configure(self, binder: Any) -> None:
        binder.bind(IMessageRepository, to=self.provide_message_repository)

    @provider
    @singleton
    def provide_message_repository(self) -> IMessageRepository:
        return AWSMessageRepository(AWS_DYNAMODB_TABLE_NAME_HISTORIES)


class AzureModule(Module):
    def configure(self, binder: Any) -> None:
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
    cloud: Optional[CloudType] = None,
) -> LocalModule | GCPModule | AWSModule | AzureModule:
    if cloud is None:
        cloud = CLOUD

    if cloud == CloudType.Local:
        return LocalModule()
    elif cloud == CloudType.GCP:
        return GCPModule()
    elif cloud == CloudType.AWS:
        return AWSModule()
    elif cloud == CloudType.AZURE:
        return AzureModule()
    raise ValueError("Invalid cloud type")
