import sys

from bones import Program

print(sys.argv)

program = Program()
program.argument('input')
program.option('--show', aliases=['-s'])

palette = program.command('palette', aliases=['pal'])
palette.argument('palette')
palette.option('--mode', aliases=['-m'], arguments=['mode', 'something else'])

program.parse(sys.argv)

print(program.input)
print(program.show)
print('command:')
print('  {}'.format(program.command.name))
print('  {}'.format(program.command.palette))
print('  {}'.format(program.command.mode))

# program = Program()
# program.option('--show', aliases=['-s'])
# program.parse(sys.argv)
# print(program.show)
