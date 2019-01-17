import sys

from bones import Program

# print(sys.argv)

# program = Program()
# program.argument('input file')
# program.option('--show', aliases=['-s'], description='Show the pixelated image')
# program.option('--thing', aliases=['-t'])
# program.option('--garbage', aliases=['-g'])
#
# palette = program.command('palette', aliases=['pal'])
# palette.argument('palette')
# palette.option('--mode', aliases=['-m'], arguments=['mode', 'something else'])
#
# program.parse(sys.argv)

# print(palette.test())
# print(program.help())
# print(program.command.help())

# print(dir(program))
# print(program.show)
# print('command:')
# print('  {}'.format(program.command.name))
# print('  {}'.format(program.command.palette))
# print('  {}'.format(program.command.mode))
#
# program = Program()
# first = program.command('first')
# second = first.command('second')
# third = second.command('third')
#
# print(third.help())

program = Program()
program.option('--force', aliases=['-f'], description='forces something to happen')
program.option('--output', aliases=['--out', '-o'], description='the output file')
program.argument('some-argument', description='an argument for this program')
program.command('action', description='performs some action')

print(program.help())
