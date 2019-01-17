import re
import utils

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
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Option():
    def __init__(self, long, aliases, arguments, description):
        self.consume = len(arguments)
        self.arguments = arguments
        self.name = long[2:]
        self.aliases = [long] + aliases
        self.description = description

class Command():
    def __init__(self, name=None, aliases=[], parent=None, description=None):
        self._arguments = []
        self._options = []
        self._commands = []
        self.name = name
        self.aliases = [name] + aliases
        self.parent = parent
        self.description = description

    def argument(self, name, description=None):
        self._arguments.append(Argument(name, description))
        setattr(self, utils.snake_case(name), None)

    def option(self, long, aliases=[], arguments=[], description=None):
        option = Option(long, aliases, arguments, description)
        self._options.append(option)
        setattr(self, utils.snake_case(option.name), None)

    def command(self, name, aliases=[], description=None):
        command = Command(name=name, aliases=aliases, parent=self, description=description)
        self._commands.append(command)
        return command

    def parse(self, argv):
        argv = self._parse_options(argv)
        argv = self._parse_arguments(argv)
        self._parse_command(argv)

    def help(self):
        usage = 'usage: '

        if self.parent:
            parents = utils.get_parents(self.parent)
            usage += '{}'.format(''.join(map(lambda p: p + ' ... ', parents)))

        arg_string = list(map(lambda a: '<{}>'.format(a.name), self._arguments))
        usage += '{} [options] {}'.format(self.name, ' '.join(arg_string))
        if len(self._commands):
            usage += ' <command>'

        options = []
        for option in self._options:
            names = ', '.join(option.aliases)
            options.append((names, option.description))

        arguments = list(((a.name, a.description) for a in self._arguments))

        commands = []
        for command in self._commands:
            names = ', '.join(command.aliases)
            commands.append((names, command.description))

        allNames = list(map(lambda o: o[0], options))
        allNames += list(map(lambda a: a[0], arguments))
        allNames += list(map(lambda c: c[0], commands))
        maxlen = max(map(lambda e: len(e), allNames), default=0)

        options = list(map(lambda o: (o[0].ljust(maxlen + 2, ' '), o[1]), options))
        arguments = list(map(lambda a: (a[0].ljust(maxlen + 2, ' '), a[1]), arguments))
        commands = list(map(lambda c: (c[0].ljust(maxlen + 2, ' '), c[1]), commands))

        if len(options):
            usage += '\n\n'
            usage += 'Options:\n'
            for option in options:
                usage += '    {}{}\n'.format(option[0], option[1] or '')

        if len(arguments):
            usage += '\n'
            usage += 'Arguments:\n'
            for argument in arguments:
                usage += '    {}{}\n'.format(argument[0], argument[1] or '')

        if len(commands):
            usage += '\n'
            usage += 'Commands:\n'
            for command in commands:
                usage += '    {}{}\n'.format(command[0], command[1] or '')

        return usage

    def _parse_options(self, argv):
        while len(argv):
            if not argv[0].startswith('-'):
                break

            arg = argv.pop(0)

            option = next((o for o in self._options if arg in o.aliases), None)

            if option:
                if option.consume == 0:
                    val = True
                elif option.consume == 1:
                    val = argv.pop(0)
                else:
                    val = argv[:option.consume]
                    argv = argv[option.consume:]

                setattr(self, utils.snake_case(option.name), val)
            else:
                raise UnknownOptionError(arg)

        return argv

    def _parse_arguments(self, argv):
        arguments = self._arguments.copy()
        while len(arguments):
            if not len(argv):
                break

            arg = argv.pop(0)
            argument = arguments.pop(0)
            setattr(self,  utils.snake_case(argument.name), arg)

        if len(arguments):
            raise MissingArgumentsError(arguments)

        return argv

    def _parse_command(self, argv):
        if len(argv):
            name = argv[0]
            command = next((c for c in self._commands if name in c.aliases), None)
            if command in self._commands:
                self.command = command
                self.command.parse(argv[1:])
            elif len(self._commands):
                raise InvalidCommandError(command)

class Program(Command):
    def __init__(self):
        super().__init__()

    def parse(self, argv):
        self.name = argv[0]
        super().parse(argv[1:])
