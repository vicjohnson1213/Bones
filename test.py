import sys

from bones import Program

# print(sys.argv)

program = Program()
program.argument('input file')
program.option('--show', aliases=['-s'], description='Show the pixelated image')
program.option('--thing', aliases=['-t'])
program.option('--garbage', aliases=['-g'])

palette = program.command('palette', aliases=['pal'])
palette.argument('palette')
palette.option('--mode', aliases=['-m'], arguments=['mode', 'something else'])

program.parse(sys.argv)

print(program.help())
print(program.command.help())
