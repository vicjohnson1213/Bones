import re

def snake_case(string):
    return re.sub(r'[^_A-Za-z1-9]+', '_', string)
