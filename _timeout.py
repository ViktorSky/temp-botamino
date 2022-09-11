from threading import Thread
from time import sleep


class TimeOut(object):


    users_dict = {}


    def time_user(
        self: object,
        userId: str,
        end: int = 5
    ) -> None:

        if userId not in self.users_dict.keys():
            self.users_dict[userId] = {
                "start": 0,
                "end": end
            }

            Thread(
                target = self.timer,
                args = [userId]
            ).start()



    def timer(
        self: object,
        userId: str
    ) -> None:

        while self.users_dict[userId]["start"] <= self.users_dict[userId]["end"]:
            self.users_dict[userId]["start"] += 1
            sleep(1)

        del self.users_dict[userId]



    def timed_out(
        self: object,
        userId: str
    ) -> bool:

        if userId in self.users_dict.keys():
            return self.users_dict[userId]["start"] >= self.users_dict[userId]["end"]

        return True