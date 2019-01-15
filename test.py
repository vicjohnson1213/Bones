import sys

from bones import Program

print(sys.argv)

program = Program()
program.argument('input')
program.option('-o, --option', consume=3)
program.option('-f, --force')

program.parse(sys.argv)

print(program.force)
print(program.option)
print(program.input)
