from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChatRecord:
    id: str
    title: str
    messages: list[dict[str, Any]] = field(default_factory=list)


class ChatRepository:
    def __init__(self) -> None:
        self.chats: dict[str, ChatRecord] = {}

    def create(self, chat_id: str, title: str) -> ChatRecord:
        record = ChatRecord(id=chat_id, title=title)
        self.chats[chat_id] = record
        return record

    def get(self, chat_id: str) -> ChatRecord | None:
        return self.chats.get(chat_id)

    def list(self) -> list[ChatRecord]:
        return list(self.chats.values())

    def append_message(self, chat_id: str, message: dict[str, Any]) -> None:
        record = self.chats.setdefault(chat_id, ChatRecord(id=chat_id, title="New chat"))
        record.messages.append(message)

    def delete(self, chat_id: str) -> None:
        self.chats.pop(chat_id, None)
