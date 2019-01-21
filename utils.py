import re

def snake_case(string):
    """Converts a string to snake case."""
    return re.sub(r'[^_A-Za-z1-9]+', '_', string)

def get_parents(command):
    """Recursively finds the name of each parent command."""
    if not command.parent:
        return [] if not command.name else [command.name]

    parents = get_parents(command.parent)
    parents.append(command.name)
    return parents

def normalize_argv(argv):
    """
    Noramlizes command-line arguments:
    -abc => -a -b -c
    --option=value => --option value
    """
    new_args = []

    for arg in argv:
        if arg.startswith('--'):
            new_args += arg.split('=', 1)
        elif arg.startswith('-'):
            new_args += map(lambda a: '-' + a, list(arg[1:]))
        else:
            new_args.append(arg)

    return new_args
