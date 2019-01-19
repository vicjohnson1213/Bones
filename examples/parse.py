# Ignore this stuff.. You can't automatically import relative packages from a parent directory.
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Start here:
from bones import Program

program = Program(sys.argv[0], 'adds two numbers together')
program.option('--left', arguments=['value'], parse=int)
program.option('--right', arguments=['value'], parse=int)

program.parse(sys.argv)

print(program.left + program.right)

# Try running these commands:
#
# python parse.py 1 2
# python parse.py a b
