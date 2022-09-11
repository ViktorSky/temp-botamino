# edited by V¡ktor

from contextlib import suppress
from pathlib import Path
from json import loads, dumps, dump
from threading import Thread
from uuid import uuid4
from time import sleep

import os

from aminofix import (
    Client,
    objects
)

from ._command import Command
from ._bot import Bot
from ._timeout import TimeOut
from ._bannedwords import BannedWords
from ._parameters import Parameters



path_utilities = "utilities"
path_amino = f'{path_utilities}/amino_list'
path_client = "client.txt"
NoneType = type(None)



with suppress(Exception):
    for i in (path_utilities, path_amino):
        Path(i).mkdir(exist_ok=True)



def print_exception(exc):
    print(repr(exc))



class BotAmino(Command, Client, TimeOut, BannedWords):

    def __init__(
        self: object,
        email: str = None,
        password: str = None,
        deviceId: str = None,
        proxies: dict = None,
        sid: str = None,
        secret: str = None,
        certificatePath: str = None,
        socketDebugging: bool = False,
        
        prefix: str = None,
        wait: int = 0,
        bio: str = "",
        spam_message: str = "You are spamming, be carefu",
        no_command_message: str = "",
        lock_message: str = "Command locked sorry",
    ) -> None:

        Command.__init__(self = self)

        Client.__init__(
            self = self,
            deviceId = deviceId,
            proxies = proxies,
            certificatePath = certificatePath,
            socketDebugging = socketDebugging
        )

        if email and (secret or password):
            self.login(
                email = email,
                password = password,
                secret = secret
            )

        elif sid:
            self.login_sid(
                SID = sid
            )

        else:
            if not os.path.exists(path_client):
                with open(path_client, 'w') as file_:
                    file_.write('email\npassword')

                print("Please enter your email and password in the file client.txt")
                print("-----end-----")
                exit(1)

            with open(path_client, "r") as file_:
                para = file_.readlines()

            self.login(
                email = para[0].strip(),
                password = para[1].strip(),
            )

        self.communaute: dict = {}
        self.botId: str = self.userId
        self.len_community: int = 0
        self.perms_list: list = []
        self.prefix: str = str(prefix or "!")
        self.activity: bool = False
        self.wait: int = int(wait)
        self.bio: str = str(bio)
        self.self_callable = False
        self.no_command_message: str = str(no_command_message)
        self.spam_message: str = str(spam_message)
        self.lock_message: str = str(lock_message)
        self.launched = False



    def tradlist(
        self: object,
        users: (tuple, list)
    ) -> list:

        objects: list = []

        for elem in users:
            with suppress(Exception):
                objectId: str = self.get_from_code(f"http://aminoapps.com/u/{elem}").objectId

                objects.append(objectId)
                continue

            objects.append(elem)

        return objects



    def add_community(
        self: object,
        comId: int
    ) -> None:

        self.communaute[comId]: Bot = Bot(
            client = self,
            community = comId,
            prefix = self.prefix,
            bio_contents = self.bio,
            activity = self.activity
        )



    def add_admin(
        self: object,
        userId: (str, list, tuple)
    ) -> None:

        assert isinstance(userId, (str, list, tuple)), "%r type is not in (str, list, tuple)" % "userId"

        if isinstance(userId, str):
            userId = [userId]

        [self.perms_list.append(id) for id in userId if id not in self.perms_list]



    def remove_admin(
        self: object,
        userId: (str, list, tuple)
    ) -> None:

        assert isinstance(userId, (str, list, tuple)), "%r type is not in (str, list, tuple)" % "userId"

        if isinstance(userId, str):
            userId = [userId]

        [self.perms_list.remove(id) for id in userId if id in self.perms_list]



    def get_community(
        self: object,
        comId: int
    ) -> Bot:

        return self.communaute.get(comId, False)



    def is_it_bot(
        self: object,
        userId: str
    ) -> bool:

        return userId == self.botId and not self.self_callable



    def is_it_admin(
        self: object,
        userId: str
    ) -> bool:

        return userId in self.perms_list



    def get_wallet_amount(
        self: object
    ) -> int:

        return self.get_wallet_info().totalCoins



    def generate_transaction_id(
        self: object
    ) -> str:

        return str(uuid4())



    def start_video_chat(
        self: object,
        comId: (str, int),
        chatId: str,
        joinType: int = 1
    ) -> None:

        data: dict = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        }

        self.send(dumps(data))

        data["o"]["channelType"] = 4
        data["t"] = 108

        self.send(dumps(data))



    def start_screen_room(
        self: object,
        comId: (str, int),
        chatId: str,
        joinType: int = 1
    ) -> None:

        data: dict = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        }

        self.send(dumps(data))

        data["o"]["channelType"] = 5
        data["t"] = 108

        self.send(dumps(data))



    def join_screen_room(
        self: object,
        comId: (str, int),
        chatId: str,
        joinType: int = 1
    ) -> None:

        data: dict = {
            "o":
                {
                    "ndcId": int(comId),
                    "threadId": chatId,
                    "joinRole": 2,
                    "id": "72446"
                },
            "t": 112
        }

        self.send(dumps(data))



    def start_voice_room(
        self: object,
        comId: (str, int),
        chatId: str,
        joinType: int = 1
    ) -> None:

        data: dict = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        }

        self.send(dumps(data))

        data["o"]["channelType"] = 1
        data["t"] = 108

        self.send(dumps(data))



    def end_voice_room(
        self: object,
        comId: (str, int),
        chatId: str,
        joinType: int = 2
    ) -> None:

        data: dict = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        }

        self.send(dumps(data))



    def show_online(
        self: object,
        comId: (str, int)
    ) -> None:

        data: dict = {
            "o": {
                "actions": ["Browsing"],
                "target": f"ndc://x{comId}/",
                "ndcId": int(comId),
                "id": "82333"
            },
            "t":304
        }

        self.send(dumps(data))



    def check(
        self: object,
        data: object,
        *can: tuple, # "staff", "admin" or "bot"
        userId: str = None
    ) -> bool:

        checks: dict = {
            "staff": data.subClient.is_in_staff,
            "admin": self.is_it_admin,
            "bot": self.is_it_bot
        }

        userId: str = userId if userId else data.authorId

        return any(checks[i](userId) for i in can)



    def check_all(
        self: object
    ) -> None:

        amino_list: object = self.sub_clients()

        for comId in amino_list.comId:
            with suppress(Exception):
                self.communaute[comId].check_in()



    def threadLaunch(
        self: object,
        comId: int,
        passive: bool = False
    ) -> None:

        self.communaute[comId]: Bot = Bot(
            client = self,
            community = comId,
            prefix = self.prefix,
            bio = self.bio,
            activity = passive
        )

        sleep(30)

        if passive:
            self.communaute[comId].passive()



    def launch(
        self: object,
        passive: bool = False
    ) -> None:

        amino_list: object = self.sub_clients()
        self.len_community: int = len(amino_list.comId)

        [
            Thread(
                target = self.threadLaunch,
                args = [comId, passive]
            ).start() for comId in amino_list.comId
        ]

        if self.launched is True:
            return

        if self.categorie_exist("command") or self.categorie_exist("answer"):
            self.launch_text_message()

        if self.categorie_exist("on_member_join_chat"):
            self.launch_on_member_join_chat()

        if self.categorie_exist("on_member_leave_chat"):
            self.launch_on_member_leave_chat()

        if self.categorie_exist("on_join_community"):
            self.launch_on_join_community()

        if self.categorie_exist("on_other"):
            self.launch_other_message()

        if self.categorie_exist("on_remove"):
            self.launch_removed_message()

        if self.categorie_exist("on_delete"):
            self.launch_delete_message()

        if self.categorie_exist("on_all"):
            self.launch_all_message()

        self.launched: bool = True



    def single_launch(
        self: object,
        comId: int,
        passive: bool = False
    ) -> None:

        amino_list: object = self.sub_clients()
        self.len_community: int = len(amino_list.comId)

        Thread(
            target = self.threadLaunch,
            args = [commu, passive]
        ).start()

        if self.launched is True:
            return

        if self.categorie_exist("command") or self.categorie_exist("answer"):
            self.launch_text_message()

        if self.categorie_exist("on_member_join_chat"):
            self.launch_on_member_join_chat()

        if self.categorie_exist("on_member_leave_chat"):
            self.launch_on_member_leave_chat()

        if self.categorie_exist("on_join_community"):
            self.launch_on_join_community()

        if self.categorie_exist("on_other"):
            self.launch_other_message()

        if self.categorie_exist("on_remove"):
            self.launch_removed_message()

        if self.categorie_exist("on_delete"):
            self.launch_delete_message()

        if self.categorie_exist("on_all"):
            self.launch_all_message()

        self.launched: bool = True



    def message_analyse(
        self: object,
        data: object,
        type: str = "command"
    ) -> None:

        with suppress(Exception):
            comId: int = data.comId
            subClient: Bot = self.get_community(comId)
            data: Parameters = Parameters(data, subClient)

            Thread(
                target = self.execute,
                args = [type, data, type]
            ).start()



    def on_member_event(
        self: object,
        data: object,
        type: str
    ) -> None:

        with suppress(Exception):
            comId: int = data.comId
            subClient = self.get_community(comId)
            args: Parameters = Parameters(data, subClient)

            if not self.check(args, "bot"):
                Thread(
                    target = self.execute,
                    args = [type, args, type]
                ).start()



    def launch_text_message(
        self: object
    ) -> None:

        def text_message(
            data: Parameters
        ) -> object:

            try: subClient: Bot = self.get_community(data.comId)
            except: return

            data: Parameters = Parameters(
                data,
                subClient
            )

            if "on_message" in self.commands.keys():
                Thread(
                    target = self.execute,
                    args = ["on_message", data, "on_message"]
                ).start()

            if self.check(data, "staff", "bot") and subClient.banned_words:
                self.check_banned_words(data)

            if not (self.timed_out(data.authorId)) and (data.message.startswith(subClient.prefix)) and (not self.check(data, "bot")):
                subClient.send_message(
                    chatId = data.chatId,
                    message = self.spam_message
                )

                return

            if ("command") in self.commands.keys() and data.message.startswith(subClient.prefix) and not self.check(data, "bot"):
                print(f"{data.author} : {data.message}")

                command: str = data.message.lower().split()[0][len(subClient.prefix):]

                if command in subClient.locked_command:
                    subClient.send_message(
                        chatId = data.chatId,
                        message = self.lock_message
                    )

                    return

                data.message = " ".join(data.message.split()[1:])

                self.time_user(
                    userId = data.authorId,
                    end = self.wait
                )

                if command.lower() in self.commands["command"].keys():
                    Thread(
                        target = self.execute,
                        args = [command, data]
                    ).start()

                elif self.no_command_message:
                    subClient.send_message(
                        chatId = data.chatId,
                        message = self.no_command_message
                    )

                    return

            elif ("answer") in self.commands.keys() and data.message.lower() in self.commands["answer"] and not self.check(data, "bot"):
                print(f"{data.author} : {data.message}")

                self.time_user(
                    userId = data.authorId,
                    end = self.wait
                )

                Thread(
                    target = self.execute,
                    args = [
                        data.message.lower(),
                        data,
                        "answer"
                    ]
                ).start()

                return

        with suppress(AttributeError):
            @self.callbacks.event("on_text_message")
            def on_text_message(
                data: objects.Event
            ) -> None:

                text_message(
                    data = data
                )

            return

        with suppress(AttributeError):
            @self.event("on_text_message")
            def on_text_message(
                data: objects.Event
            ) -> None:

                text_message(
                    data = data
                )

            return



    def launch_other_message(
        self: object
    ) -> None:

        for type_name in (
            "on_strike_message",
            "on_voice_chat_not_answered",
            "on_voice_chat_not_cancelled",
            "on_voice_chat_not_declined",
            "on_video_chat_not_answered",
            "on_video_chat_not_cancelled",
            "on_video_chat_not_declined",
            "on_voice_chat_start",
            "on_video_chat_start",
            "on_voice_chat_end",
            "on_video_chat_end",
            "on_screen_room_start",
            "on_screen_room_end",
            "on_avatar_chat_start",
            "on_avatar_chat_end"
        ):

            with suppress(AttributeError):
                @self.callbacks.event(type_name)
                def on_other_message(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_other"
                    )

                continue

            with suppress(AttributeError):
                @self.event(type_name)
                def on_other_message(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_other"
                    )

                continue



    def launch_all_message(
        self: object
    ) -> None:

        with suppress(AttributeError):
            for x in (self.chat_methods.keys()):
                @self.event(self.chat_methods[x].__name__)
                def on_all_message(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_all"
                    )

            return

        with suppress(AttributeError):
            for x in (self.callbacks.chat_methods):
                @self.callbacks.event(self.callbacks.chat_methods[x].__name__)
                def on_all_message(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_all"
                    )

            return



    def launch_delete_message(
        self: object
    ) -> None:

        with suppress(AttributeError):
            @self.callbacks.event("on_delete_message")
            def on_delete_message(
                data: objects.Event
            ) -> None:

                self.message_analyse(
                    data = data,
                    type = "on_delete"
                )

        with suppress(AttributeError):
            @self.event("on_delete_message")
            def on_delete_message(
                data: objects.Event
            ) -> None:

                self.message_analyse(
                    data = data,
                    type = "on_delete"
                )



    def launch_removed_message(
        self: object
    ) -> None:

        for type_name in (
            "on_chat_removed_message",
            "on_text_message_force_removed",
            "on_text_message_removed_by_admin",
            "on_delete_message"
        ):

            with suppress(AttributeError):
                @self.callbacks.event(type_name)
                def on_chat_removed(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_remove"
                    )

                continue

            with suppress(AttributeError):
                @self.event(type_name)
                def on_chat_removed(
                    data: objects.Event
                ) -> None:

                    self.message_analyse(
                        data = data,
                        type = "on_remove"
                    )

                continue



    def launch_on_member_join_chat(
        self: object
    ) -> None:

        with suppress(AttributeError):
            @self.callbacks.event("on_group_member_join")
            def on_group_member_join(
                data: objects.Event
            ) -> None:

                self.on_member_event(
                    data = data,
                    type = "on_member_join_chat"
                )

        with suppress(AttributeError):
            @self.event("on_group_member_join")
            def on_group_member_join(
                data: objects.Event
            ) -> None:

                self.on_member_event(
                    data = data,
                    type = "on_member_join_chat"
                )



    def launch_on_member_leave_chat(
        self: object
    ) -> None:

        with suppress(AttributeError):
            @self.callbacks.event("on_group_member_leave")
            def on_group_member_leave(
                data: objects.Event
            ) -> None:

                self.on_member_event(
                    data = data,
                    type = "on_member_leave_chat"
                )

        with suppress(AttributeError):
            @self.event("on_group_member_leave")
            def on_group_member_leave(
                data: objects.Event
            ) -> None:

                self.on_member_event(
                    data = data,
                    type = "on_member_leave_chat"
                )



    def launch_on_join_community(
        self: object
    ) -> None:

        pass
        # waiting for  amino.fix