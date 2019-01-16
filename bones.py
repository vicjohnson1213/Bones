class BonesError(Exception):
    pass

class UnknownOptionError(BonesError):
    def __init__(self, option):
        self.option = option

class MissingArgumentsError(BonesError):
    def __init__(self, args):
        self.arguments = args

class InvalidCommandError(BonesError):
    def __init__(self, command):
        self.command = command

class Argument():
    def __init__(self, name):
        self.name = name

class Option():
    def __init__(self, long, aliases, arguments):
        self.consume = len(arguments)
        self.arguments = arguments
        self.name = long[2:]
        self.aliases = aliases

class Command():
    def __init__(self, name=None, aliases=[]):
        self._arguments = []
        self._options = []
        self._commands = []
        self.name = name
        self.aliases = aliases

    def argument(self, name):
        self._arguments.append(Argument(name))
        setattr(self, name, None)

    def option(self, long, aliases=[], arguments=[]):
        option = Option(long, aliases, arguments)
        self._options.append(option)
        setattr(self, option.name, None)

    def command(self, name, aliases=[]):
        command = Command(name=name, aliases=aliases)
        self._commands.append(command)
        return command

    def parse(self, argv):
        argv = self._parse_options(argv)
        argv = self._parse_arguments(argv)
        self._parse_command(argv)

    def _parse_options(self, argv):
        while len(argv):
            if not argv[0].startswith('-'):
                break

            arg = argv.pop(0)

            option = next((o for o in self._options if arg == o.name or arg in o.aliases), None)

            if option:
                if option.consume == 0:
                    val = True
                elif option.consume == 1:
                    val = argv.pop(0)
                else:
                    val = argv[:option.consume]
                    argv = argv[option.consume:]

                setattr(self, option.name, val)
            else:
                raise UnknownOptionError(arg)

        return argv

    def _parse_arguments(self, argv):
        while len(self._arguments):
            if not len(argv):
                break

            arg = argv.pop(0)
            argument = self._arguments.pop(0)
            setattr(self, argument.name, arg)

        if len(self._arguments):
            raise MissingArgumentsError(self._arguments)

        return argv

    def _parse_command(self, argv):
        if len(argv):
            name = argv[0]
            command = next((c for c in self._commands if name == c.name or name in c.aliases), None)
            if command in self._commands:
                self.command = command
                self.command.parse(argv[1:])
            elif len(self._commands):
                raise InvalidCommandError(command)

class Program(Command):
    def __init__(self):
        super().__init__()

    def parse(self, argv):
        super().parse(argv[1:])
