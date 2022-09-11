from contextlib import suppress
from unicodedata import normalize
from string import punctuation


class BannedWords(object):

    def filtre_message(
        self: object,
        message: str,
        code: str
    ) -> str:

        text: str = normalize('NFD', message).encode(code, 'ignore').decode("utf8").strip()

        return text.lower().translate(str.maketrans("", "", punctuation))



    def check_banned_words(
        self: object,
        data: object,
        staff: bool = True
    ) -> None:

        for word in ("ascii", "utf8"):
            with suppress(Exception):
                messages: list = self.filtre_message(data.message, word).split()

                if messages == [""]:
                    return None

                for word in messages:
                    if word in data.subClient.banned_words:
                        data.subClient.delete_message(data.chatId, data.messageId, reason = f"Banned word : {word}", asStaff = staff)

                        [data.subClient.delete_message(data.chatId, data.messageId, reason = f"Banned word : {word}", asStaff = staff) for word in texts if (word in data.subClient.banned_words)]