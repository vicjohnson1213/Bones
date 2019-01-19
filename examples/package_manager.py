# Ignore this stuff.. You can't automatically import relative packages from a parent directory.
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Start here:
from bones import Program

program = Program(sys.argv[0], description='A pretend package manager')

install = program.command('install', aliases=['i', 'in'], description='install one or more packages')
install.option('--globally', aliases=['-g'], description='install these packages globally')
install.argument('packages', description='the packages to install', variadic=True)

uninstall = program.command('uninstall', aliases=['u', 'un'], description='unstalls one or more packages')
uninstall.option('--globally', aliases=['-g'], description='uninstall these packages globally')
uninstall.argument('packages', description='the packages to uninstall', variadic=True)

list = program.command('list', aliases=['l', 'ls'], description='lists installed packages')
list.option('--globally', aliases=['-g'], description='list globally installed packages')

program.parse(sys.argv)

if (program.command.name == 'install'):
    print('installing: {}'.format(program.command.packages))
    print('globally: {}'.format(program.command.globally))

elif (program.command.name == 'uninstall'):
    print('uninstalling: {}'.format(program.command.packages))
    print('globally: {}'.format(program.command.globally))

elif (program.command.name == 'list'):
    print('list some imaginary packages')
    print('globally: {}'.format(program.command.globally))

# Try running these commands:
#
# python package_manager.py install pack1
# python package_manager.py i -g pack1 pack2 pack3
#
# python package_manager.py uninstall -g pack1
# python package_manager.py un pack1 pack2
#
# python package_manager.py list
# python package_manager.py l -g
