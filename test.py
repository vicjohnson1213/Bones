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
#
# print(program.help())
# print(program.command.help())

program = Program('prog')
program.option('--force', aliases=['-f'], description='forces something to happen')
program.option('--output', aliases=['--out', '-o'], description='the output file')
program.argument('some-argument', description='an argument for this program')
action = program.command('action', description='performs some action')
action.option('--something', description='a description for this option')
action.argument('input', 'an input file for this command')

print(action.help())
# print(program.help())
