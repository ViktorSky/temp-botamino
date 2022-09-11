from contextlib import contextmanager
from aminofix import objects
from json import dumps
from ._bot import Bot


class Parameters:

    __slots__ = (
        "author",
        "authorIcon",
        "authorId",
        "chatId",
        "chatType",
        "comId",
        "info",
        "json",
        "level",
        "mentions",
        "message",
        "messageId",
        "messageType",
        "replyAuthor",
        "replyAuthorId",
        "replyId",
        "replyMsg",
        "replySrc",
        "reputation",
        "subClient"
    )


    def __init__(
        self: object,
        data: objects.Event,
        subClient: Bot
    ) -> None:

        self.author: str = data.message.author.nickname
        self.authorIcon: str = data.message.author.icon
        self.authorId: str = data.message.author.userId
        self.level = data.message.json.get("author", {}).get("level", None)
        self.reputation = data.message.json.get("author", {}).get("reputation", None)

        self.chatId: str = data.message.chatId
        self.chatType: int = data.threadType
        self.comId: int = data.comId

        self.message: str = data.message.content
        self.messageId: str = data.message.messageId
        self.messageType: str = data.message.messageType
        self.replyId: str = data.message.extensions.get("replyMessage", {}).get("messageId", None)
        self.replyAuthor: str = data.message.author.nickname
        self.replyAuthorId: str = data.message.author.userId
        self.replyMsg: str = data.message.extensions.get("replyMessage", {}).get("content", "")
        self.replySrc: str = data.message.extensions.get('replyMessage', {}).get("mediaValue", "").replace('_00.', '_hq.')
        self.mentions: list = data.message.mentionUserIds or []

        self.subClient: Bot = subClient

        self.json: dict = data.json
        self.info: objects.Event = data



    @contextmanager
    def typing(
        self: object
    ) -> None:

        data = {
            "o": {
                "actions": ["Typing"],
                "target": f"ndc://x{self.comId}/chat-thread/{self.chatId}",
                "ndcId": self.comId,
                "params": {
                    "threadType": self.chatType,
                },
                "id": "2713213"
            },
            "t": 304
        }

        try:
            self.subClient.send(dumps(data))
            yield
        finally:
            data["t"] = 306
            self.subClient.send(dumps(data))



    @contextmanager
    def recording(
        self: object
    ) -> None:

        data = {
            "o": {
                "actions": ["Recording"],
                "target": f"ndc://x{self.comId}/chat-thread/{self.chatId}",
                "ndcId": self.comId,
                "params": {
                    "threadType": self.chatType,
                },
                "id": "161486614"
            },
            "t": 304
        }

        try:
            self.subClient.send(dumps(data))
            yield
        finally:
            data["t"] = 306
            self.subClient.send(dumps(data))
