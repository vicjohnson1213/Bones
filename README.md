# Bones

> Bones is a bare-bones, opinionated command-line options parser for python.

# Usage

- [`Program()`](#program)
- [`program.option(long, aliases=[], arguments=[], description=None)`](#options)
- [`program.argument(name, description=None)`](#arguments)
- [`program.command(name, aliases=[], description=None)`](#commands)
- [`program.parse(argv)`](#parse)
- [`program.help()`](#help)

## Program

`Program(name, description=None)`

**Returns:** A new program that options/arguments/commands can be added to.

| Argument | Description | Default |
|----------|-------------|---------|
| `name` | The `name` argument is required and will be displayed in the output of the default help text. This should usually be `sys.argv[0]`. | Required |
| `description` | The `description` argument is optional and will be displayed in the output of the default help text. | `None` |

Creates a new options parser. This parser will serve as the root of all other options, arguments, and commands.

```python
from Bones import Program
program = Program('prog')
```

## Options

`program.option(long, aliases=[], arguments=[], description=None)`

| Argument | Description | Default |
|----------|-------------|---------|
| `long` | The `long` argument is required and is meant to be the long form of the option (i.e. `--option`). This will also determine the name of the attribute used to access the parsed value for this option. The `long` argument is expected to begin with two hyphens (`--XXXXX`) | Required |
| `aliases` | The `aliases` argument is optional and can be used to define any alternate option names or flags that can be used for this option. | `[]` |
| `arguments` | The `arguments` argument is optional and can be used to name any arguments that this option will consume. This argument will also determine how many command-line arguments after this option are consumed. | `[]` |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |

The values for a parsed option are available via an attribute on the program named by the `long` argument. If an option doesn't consume any arguments, it's value will be set to `True` if it is present. If there is a single argument, the value will simply be what is passed into the option. If there is more than one argument, they will be available as a list of values. Any options that aren't used in the execution of the program will have a value of `None`.

**Note:** Any non-alphanumeric characters in the `long` argument will be converted to underscores for accessing the value (e.g. `--some-option` will be accessible via `program.some_option`).

```python
program = Program('prog')
program.option('--force', aliases=['-f'])
program.option('--input-file', aliases=['-i', '--in'], arguments=['input-file'])
program.parse(sys.argv) # ['program.py', '-f', '--in', 'some-file.txt']

print(program.force) # True
print(program.input_file) # 'some-file.txt'
```

## Arguments

`program.argument(name, description=None, variadic=False)`

| Argument | Description | Default |
|----------|-------------|---------|
| `name` | The `name` argument is required and will act as the attribute that the value for this argument can be accessed through. | Required |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |
| `variadic` | The `variadic` argument is optional allows for a variable number of arguments to be passed into the program. If `variadic` is set to `True`, it will disallow any other arguments or commands in the program. | `False` |

The value for a parsed argument are available via an attribute on the program named by the `name` argument. If this argument is variadic, the values will be available as a list of all values passed in.

**Note:** Any non-alphanumeric characters in the `name` argument will be converted to underscores for accessing the value (e.g. `some-argument` will be accessible via `program.some_argument`).

```python
program = Program('prog')
program.argument('input file')
program.argument('output file')
program.parse(sys.argv) # ['program.py', 'some-input-file.txt', 'some-output-file.txt']

print(program.input_file) # 'some-input-file.txt'
print(program.output_file) # 'some-output-file.txt'
```

## Commands

`program.command(name, aliases=[], description=None)`

**Returns**: The new command so options/arguments/commands can be added to it.

| Argument | Description | Default |
|----------|-------------|---------|
| `name` | The `name` argument is required and is used to determine which command is being used. | Required |
| `aliases` | The `aliases` argument is optional and is used to specify any additional names that this command can be run with. | `[]` |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |

The sub-command and its options/arguments are accessible via the `program.command` attribute.

**Note:** Since a sub-command is always accessed via the `program.command` attribute, non-alphanumeric characters in the name ***are not*** converted to underscores.

```python
program = Program('prog')

add = program.command('add', aliases=['a'])
add.argument('left')
add.argument('right')

subtract = program.command('subtract', aliases=['s', 'sub'])
add.argument('left')
add.argument('right')

program.parse(sys.argv) # ['program.py', 'add', '1', '2']

print(program.command.name) # 'add'
print(program.command.left) # '1'
print(program.command.right) # '2'
```

## Parse

`program.parse(argv)`

Parses the command line arguments and sets up the program for the rest of the execution.

| Argument | Description | Default |
|----------|-------------|---------|
| `argv` | The `argv` argument should be the raw command line arguments for the program (typically `sys.argv`). Bones assumes that the script name is the first raw argument. | Required |

Once parse runs, the program should be populated with the data supplied in the command-line arguments.

```python
program = Program('prog')
program.argument('some-argument')
program.parse(sys.argv) # ['program.py', 'argument #1']

print(program.some_argument) # 'argument #1'
```

## Help

`program.help()`

**Returns:** The auto-generated help text for the command. Each sub-command will have its own help text.

```python
program = Program('prog')
program.option('--force', aliases=['-f'], description='forces something to happen')
program.option('--output', aliases=['--out', '-o'], description='the output file')
program.argument('some-argument', description='an argument for this program')

action = program.command('action', description='performs some action')
action.option('--something', description='a description for this option')
action.argument('input', 'an input file for this command')

print(program.help())

# usage: prog [options] <some-argument> {command}
#
# Options:
#     --force, -f          forces something to happen
#     --output, --out, -o  the output file
#
# Arguments:
#     some-argument        an argument for this program
#
# Commands:
#     action               performs some action

print(action.help())

# usage: prog ... action [options] <input>
#
# Options:
#     --something  a description for this option
#
# Arguments:
#     input        an input file for this command
```
