from threading import Thread
from time import sleep


class TimeOut(object):


    users_dict = {}


    def time_user(
        self: object,
        uid: str,
        end: int = 5
    ) -> None:

        if uid not in self.users_dict.keys():
            self.users_dict[uid] = {
                "start": 0,
                "end": end
            }

            Thread(
                target = self.timer,
                args = [uid]
            ).start()


    def timer(
        self: object,
        uid: str
    ) -> None:

        while self.users_dict[uid]["start"] <= self.users_dict[uid]["end"]:
            self.users_dict[uid]["start"] += 1
            sleep(1)

        del self.users_dict[uid]


    def timed_out(
        self: object,
        uid: str
    ) -> bool:

        if uid in self.users_dict.keys():
            return self.users_dict[uid]["start"] >= self.users_dict[uid]["end"]

        return True