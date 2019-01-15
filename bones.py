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

    def option(self, flags, consume=0):
        self._options.append(Option(flags, consume))

    def command(self, name):
        self._commands[name] = Command(name=name)
        return self._commands[name]

    def parse(self, argv):
        while len(argv):
            arg = argv.pop(0)

            if arg[0] == '-':
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
                    continue

            if arg in self._commands:
                setattr(self, 'command', self._commands[arg])
                self._commands[arg].parse(argv)

            if len(self._arguments):
                argument= self._arguments.pop(0)
                setattr(self, argument.name, arg)

class Program(Command):
    def __init__(self):
        super().__init__()

    def parse(self, argv):
        super().parse(argv[1:])
