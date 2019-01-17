import re

def snake_case(string):
    return re.sub(r'[^_A-Za-z1-9]+', '_', string)

def get_parents(command):
    if not command.parent:
        return [] if not command.name else [command.name]

    parents = get_parents(command.parent)
    parents.append(command.name)
    return parents

def normalize_argv(argv):
    new_args = []

    for arg in argv:
        if arg.startswith('--'):
            new_args += arg.split('=')
        elif arg.startswith('-'):
            new_args += map(lambda a: '-' + a, list(arg[1:]))
        else:
            new_args.append(arg)

    return new_args
