from inspect import getfullargspec


class Command(object):

    def __init__(self) -> None:

        self.commands: dict = {}
        self.conditions: dict = {}


    def execute(
        self,
        commande: str,
        data: object,
        type: str = "command"
    ) -> None:

        command: object = self.commands[type][commande]
        args: list = getfullargspec(command).args
        args.pop(0)
        condition = True

        if self.conditions[type].get(commande, None):
            if not self.conditions[type][commande](data):
                return None

        self.commands[type][commande](data, **{key: value for key, value in zip(args, data.message.split()[0:len(args)])})


    def categorie_exist(
        self,
        type: str
    ) -> bool:

        return type in self.commands.keys()


    def add_categorie(
        self,
        type: str
    ) -> None:

        if type not in self.commands.keys():
            self.commands[type] = {}


    def add_condition(
        self,
        type: str
    ) -> None:

        if type not in self.conditions.keys():
            self.conditions[type] = {}


    def functionexists(
        self,
        name: str,
        type: str = None
    ) -> bool:
        # New

        if isinstance(name, str):
            return (name.lower() in self.commands.get(type, {})) if type is not None else (name.lower() in self.commands)

        return name in self.commands.values()


    def iscommand(
        self,
        name: (str, object)
    ) -> bool:
        # New

        return self.functionexists(name, "command")


    def isanswer(
        self,
        name: (str, object)
    ) -> bool:
        # New

        return self.functionexists(name, "answer")


    def commands_list(self) -> list:
        return [command for command in self.commands["command"].keys()]


    def answer_list(self) -> list:
        return [answer for answer in self.commands["answser"].keys()]


    def command(
        self,
        name: str = None,
        condition: str = None
    ) -> object:

        type: str = "command"
        self.add_categorie(type)
        self.add_condition(type)

        if isinstance(name, str):
            name: list = [name]

        elif not name:
            name: list = []

        def add_command(function: object) -> object:
            if not name:
                name.append(function.__name__)

            for command in name:
                assert not self.iscommand(command), "%r command already exists." % command

                self.commands[type][command.lower()] = function

            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition

            return function

        return add_command


    def answer(
        self,
        name: str,
        condition: object = None
    ) -> object:

        type: str = "answer"
        self.add_categorie(type)
        self.add_condition(type)

        if isinstance(name, str):
            name: list = [name]

        elif not name:
            name: list = []

        def add_command(function: object) -> object:
            if not name:
                name.append(function.__name__)

            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition

            for command in name:
                assert not self.isanswer(command), "%r answer already exists." % command

                self.commands[type][command.lower()] = function

            return function

        return add_command


    def on_member_join_chat(
        self,
        condition: object = None
    ) -> object:

        type: str = "on_member_join_chat"
        self.add_categorie(type)
        self.add_condition(type)
        
        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_member_leave_chat(
        self,
        condition: object = None
    ) -> object:

        type: str = "on_member_leave_chat"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_message(
        self,
        condition: object = None
    ) -> object:

        type = "on_message"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function):
            self.commands[type][type] = function

            return function

        return add_command


    def on_other(
        self,
        condition: object = None
    ) -> object:

        type = "on_other"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_delete(
        self,
        condition: object = None
    ) -> object:

        type = "on_delete"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_remove(
        self,
        condition: object = None
    ) -> object:

        type = "on_remove"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_all(
        self,
        condition: object = None
    ) -> object:

        type = "on_all"
        self.add_categorie(type)
        self.add_condition(type)

        assert not self.functionexists(type, type), "%r event is already exists." % type

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(function: object) -> object:
            self.commands[type][type] = function

            return function

        return add_command


    def on_event(
        self,
        name: str,
        condition: object = None
    ) -> object:

        type = "on_event"
        self.add_categorie(type)
        self.add_condition(type)

        if isinstance(name, str):
            name = [name]

        elif not name:
            name = []

        for command in name:
            assert not self.functionexists(command, type), "%r is already exists." % ("%s.%s" % (type, command))

        def add_command(function: object) -> object:
            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition

            for command in name:
                self.commands[type][command] = function

            return function

        return add_command
