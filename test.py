import sys

from bones import Program

# print(sys.argv)

program = Program()
program.argument('input file')
program.option('--show', aliases=['-s'])
program.option('--thing', aliases=['-t'])
program.option('--garbage', aliases=['-g'])

palette = program.command('palette', aliases=['pal'])
palette.argument('palette')
palette.option('--mode', aliases=['-m'], arguments=['mode', 'something else'])

program.parse(sys.argv)

program.help()
# program.command.help()

# print(dir(program))
# print(program.show)
# print('command:')
# print('  {}'.format(program.command.name))
# print('  {}'.format(program.command.palette))
# print('  {}'.format(program.command.mode))

# program = Program()
# program.option('--show', aliases=['-s'])
# program.parse(sys.argv)
# print(program.show)
