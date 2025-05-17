import sqlite3
from pathlib import Path

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.infrastructure.repository.message.util import current_time_iso
from app.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class SQLiteMessageRepository(IMessageRepository):
    def __init__(self, db_file: Path | str) -> None:
        self._conn = sqlite3.connect(db_file, check_same_thread=False)
        self._create_table()

    def _create_table(self) -> None:
        """メッセージを保存するためのテーブルを作成する"""
        cursor = self._conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                update_at TEXT NOT NULL
            )
        """
        )
        self._conn.commit()

    def upsert(self, message: Message) -> None:
        """メッセージを上書きまたは新規作成する

        Args:
            message (Message): 保存するメッセージ
        """
        message_dict = message.to_repository()

        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (id, content, update_at)
            VALUES (?, ?, ?)
        """,
            (
                message_dict["id"],
                message_dict["content"],
                current_time_iso(),
            ),
        )
        self._conn.commit()

    def find_all(self, limit: int = 10) -> list[Message]:
        """保存されているメッセージを取得する

        Args:
            limit (int, optional): 取得するメッセージの最大数. Defaults to 10.

        Returns:
            list[Message]: メッセージのリスト
        """
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT * FROM messages
            ORDER BY update_at DESC
            LIMIT ?
        """,
            (limit,),
        )
        result = cursor.fetchall()

        messages = []
        for row in result:
            try:
                message = Message(row[1], id=row[0])
                messages.append(message)
            except Exception as e:
                logger.error(f"SQLiteからのデータの読み込みに失敗しました。: {e}")
                continue
        return messages
