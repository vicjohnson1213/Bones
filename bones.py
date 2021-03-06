import re
import utils

class BonesError(Exception):
    """Base error for this package."""
    pass

class UnknownOptionError(BonesError):
    """Error for options that weren't set up through the `program.option(...)` method."""
    def __init__(self, option):
        self.option = option

class MissingArgumentsError(BonesError):
    """Error for positional arguments that weren't supplied."""
    def __init__(self, args):
        self.arguments = args

class InvalidCommandError(BonesError):
    """Error for a command that doesn't exist in the program."""
    def __init__(self, command):
        self.command = command

class VariadicArgumentPositionError(BonesError):
    """Error for when an argument or command is added after a variadic argument."""
    def __init__(self, argument):
        self.argument = argument

class ParseError(BonesError):
    """Error for when an automatic parse of an option fails."""
    def __init__(self, innerException, arg):
        self.innerException = innerException
        self.argument = arg

class Argument():
    """A positional argument in the program."""
    def __init__(self, name, description, variadic, parse):
        self.name = name
        self.description = description
        self.variadic = variadic
        self.parse = parse

class Option():
    """An option or flag in the program."""
    def __init__(self, long, aliases, arguments, description, parse):
        self.consume = len(arguments)
        self.arguments = arguments
        self.name = long[2:]
        self.aliases = [long] + aliases
        self.description = description
        self.parse = parse

class Command():
    """A command that can contain options, argument, and sub-commands."""
    def __init__(self, name, aliases=[], parent=None, description=None):
        self._arguments = []
        self._options = []
        self._commands = []
        self.name = name
        self.aliases = [name] + aliases
        self.parent = parent
        self.description = description

    def option(self, long, aliases=[], arguments=[], description=None, parse=None):
        """Adds a new option or flag to this command."""
        option = Option(long, aliases, arguments, description, parse)
        self._options.append(option)
        setattr(self, utils.snake_case(option.name), None)

    def argument(self, name, description=None, variadic=False, parse=None):
        """Adds a new positional argument to this command."""
        if any(a.variadic for a in self._arguments):
            raise VariadicArgumentPositionError(name)

        self._arguments.append(Argument(name, description, variadic, parse))
        setattr(self, utils.snake_case(name), None)

    def command(self, name, aliases=[], description=None):
        """Adds and returns a new sub-command to this command."""
        if any(a.variadic for a in self._arguments):
            raise VariadicArgumentPositionError(name)

        command = Command(name=name, aliases=aliases, parent=self, description=description)
        self._commands.append(command)
        return command

    def parse(self, argv):
        """Parse a set of arguments for this command."""
        argv = utils.normalize_argv(argv)
        argv = self._parse_options(argv)
        argv = self._parse_arguments(argv)
        self._parse_command(argv)

    def help(self):
        """Builds and returns default help text for this command."""
        usage = '{}\n\n'.format(self.name)

        if self.description:
            usage += '{}\n\n'.format(self.description)

        usage += 'usage: '

        if self.parent:
            parents = utils.get_parents(self.parent)
            usage += '{}'.format(''.join(map(lambda p: p + ' ... ', parents)))

        arg_strings = []
        for arg in self._arguments:
            s = '<{}'.format(arg.name)
            s += '...>' if arg.variadic else '>'
            arg_strings.append(s)

        usage += '{} [options] {}'.format(self.name, ' '.join(arg_strings))
        if len(self._commands):
            usage += ' {command}'

        usage += '\n'

        options = []
        for option in self._options:
            names = ', '.join(option.aliases)
            args = ' '.join('<{}>'.format(a) for a in option.arguments)
            s = '{} {}'.format(names, args)
            options.append((s, option.description))

        arguments = []
        for arg in self._arguments:
            s = arg.name
            if arg.variadic:
                s += '...'
            arguments.append((s, arg.description))

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
            usage += '\n'
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
        """Parses all options for this command."""
        while len(argv):
            if not argv[0].startswith('-'):
                break

            arg = argv.pop(0)

            option = next((o for o in self._options if arg in o.aliases), None)

            if option:
                if option.consume == 0:
                    val = True
                elif option.consume == 1:
                    unparsed_val = argv.pop(0)
                else:
                    unparsed_val = argv[:option.consume]
                    argv = argv[option.consume:]

                if option.parse and option.consume >= 1:
                    try:
                        val = option.parse(unparsed_val) if option.consume >= 1 else list(map(option.parse, unparsed_val))
                    except Exception as e:
                        raise ParseError(e, unparsed_val)
                else:
                    val = unparsed_val

                setattr(self, utils.snake_case(option.name), val)
            else:
                raise UnknownOptionError(arg)

        return argv

    def _parse_arguments(self, argv):
        """Parses all positional arguments for this command."""
        arguments = self._arguments.copy()
        while len(arguments):
            if not len(argv):
                break

            argument = arguments.pop(0)
            val = argv if argument.variadic else argv.pop(0)

            if argument.parse:
                try:
                    if argument.variadic:
                        val = list(map(argument.parse, val))
                    else:
                        val = argument.parse(val)
                except Exception as e:
                    raise ParseError(e, val)

            setattr(self,  utils.snake_case(argument.name), val)

        if len(arguments):
            raise MissingArgumentsError(arguments)

        return argv

    def _parse_command(self, argv):
        """
        Parses the sub-command for this command and initiates any parsing that
        the sub-command may need to do.
        """
        if len(argv):
            name = argv[0]
            command = next((c for c in self._commands if name in c.aliases), None)
            if command in self._commands:
                self.command = command
                self.command.parse(argv[1:])
            elif len(self._commands):
                raise InvalidCommandError(command)

class Program(Command):
    """The main program for bones. Just a wrapper around the Command class."""
    def __init__(self, name, description=None):
        super().__init__(name, description=description)

    def parse(self, argv):
        super().parse(argv[1:])
