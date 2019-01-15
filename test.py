import sys

from bones import Program

print(sys.argv)

program = Program()
program.argument('input')
program.option('-s, --show')

palette = program.command('palette')
palette.argument('palette')
palette.option('-m, --mode', consume=1)


program.parse(sys.argv[1:])

print(program.input)
print(program.show)
print('command:')
print('  ' + program.command.name)
print('  ' + program.command.palette)
print('  ' + program.command.mode)

# program = Program()
# program.option('-r, --ree', consume=3)
#
# program.parse(sys.argv)
#
# print(program.ree)
