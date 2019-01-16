import re

def snake_case(string):
    return re.sub(r'[^_A-Za-z1-9]+', '_', string)

def get_parents(command):
    if not command.parent:
        return [] if not command.name else [command.name]

    parents = get_parents(command.parent)
    parents.append(command.name)
    return parents
