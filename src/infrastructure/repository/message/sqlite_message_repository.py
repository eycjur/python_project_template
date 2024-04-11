import sqlite3

from src.domain.message.message import Message
from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.util import current_time_iso
from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class SQLiteMessageRepository(IMessageRepository):
    def __init__(self, db_file: str) -> None:
        self._conn = sqlite3.connect(db_file)
        self._create_table()

    def _create_table(self) -> None:
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
            message = Message(row[1], id=row[0])
            messages.append(message)
        return messages
