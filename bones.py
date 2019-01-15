class BonesError(Exception):
    pass

class Argument():
    def __init__(self, name):
        self.name = name

class Option():
    def __init__(self, flags, consume):
        self.consume = consume

        flags = flags.split(',')
        for flag in flags:
            flag = flag.strip()
            if flag.startswith('--'):
                self.long_flag = flag
                self.name = flag[2:]
            else:
                self.short_flag = flag

class Command():
    def __init__(self, name=None):
        self._arguments = []
        self._options = []
        self._commands = {}
        self.name = name

    def argument(self, name):
        self._arguments.append(Argument(name))
        setattr(self, name, None)

    def option(self, flags, consume=0):
        option = Option(flags, consume)
        self._options.append(option)
        setattr(self, option.name, None)

    def command(self, name):
        self._commands[name] = Command(name=name)
        return self._commands[name]

    def parse(self, argv):
        argv = self._parse_options(argv)
        argv = self._parse_arguments(argv)

        if len(argv):
            command = argv[0]
            if command in self._commands:
                self.command = self._commands[command]
                self.command.parse(argv[1:])
            elif len(self._commands):
                print('ERROR: invalid command: {}'.format(command))
            else:
                print('ERROR: too many arguments: {}'.format(argv))

    def _parse_options(self, argv):
        while len(argv):
            if not argv[0].startswith('-'):
                break

            arg = argv.pop(0)

            option = next((o for o in self._options if o.short_flag == arg or o.long_flag == arg), None)

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
                print('ERROR: unknown option: {}'.format(arg))

        return argv

    def _parse_arguments(self, argv):
        while len(self._arguments):
            if not len(argv):
                break

            arg = argv.pop(0)
            argument = self._arguments.pop(0)
            setattr(self, argument.name, arg)

        if len(self._arguments):
            print('ERROR: missing arguments: {}'.format(self._arguments))

        return argv

class Program(Command):
    def __init__(self):
        super().__init__()

    def parse(self, argv):
        super().parse(argv[1:])
