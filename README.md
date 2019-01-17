# Bones

> A bare-bones, opinionated command-line options parser for python.

## Usage

### `Program()`

Creates a new options parser. This parser will serve as the root of all other options, arguments, and commands.

```python
from Bones improt Program
program = Program()
```

#### Methods

#### `program.option(long, aliases=[], arguments=[], description=None)`

Adds a new command-line option or flag to the program.

| Argument | Description | Default |
|----------|-------------|---------|
| `long` | The `long` argument is required and is meant to be the long form of the option (i.e. `--option`). This will also determine the name of the attribute used to access the parsed value for this option. The `long` argument is expected to begin with two hyphens (`--XXXXX`) | Required |
| `aliases` | The `aliases` argument is optional and can be used to define any alternate option names or flags that can be used for this option. | `[]` |
| `arguments` | The `arguments` argument is optional and can be used to name any arguments that this option will consume. This argument will also determine how many command-line arguments after this option are consumed. | `[]` |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |

The values for a parsed option are available via an attribute on the program named by the `long` argument. If an option doesn't consume any arguments, it's value will be set to `True` if it is present. If there is a single argument, the value will simply be what is passed into the option. If there is more than one argument, they will be available as a list of values. Any options that aren't used in the execution of the program will have a value of `None`.

**Note:** Any non-alphanumeric characters in the `long` argument will be converted to underscores for accessing the value (e.g. `--some-option` will be accessible via `program.some_option`).

```python
program = Program()
program.option('--force', aliases=['-f'])
program.option('--input-file', aliases=['-i', '--in'], arguments=['input-file'])
program.parse(sys.argv) # ['program.py', '-f', '--in', 'some-file.txt']

print(program.force) # True
print(program.input_file) # 'some-file.txt'
```

#### `program.argument(name, description=None)`

Adds a new positional argument to the program.

| Argument | Description | Default |
|----------|-------------|---------|
| `name` | The `name` argument is required and will act as the attribute that the value for this argument can be accessed through. | Required |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |

The value for a parsed argument are available via an attribute on the program named by the `name` argument.

**Note:** Any non-alphanumeric characters in the `name` argument will be converted to underscores for accessing the value (e.g. `some-argument` will be accessible via `program.some_argument`).

```python
program = Program()
program.argument('input file')
program.argument('output file')
program.parse(sys.argv) # ['program.py', 'some-input-file.txt', 'some-output-file.txt']

print(program.input_file) # 'some-input-file.txt'
print(program.output_file) # 'some-output-file.txt'
```

#### `program.command(name, aliases=[], description=None)`

Adds a new sub-command to the program and returns the new command so options/arguments/sub-commands can be added to it. Sub-commands can be nested indefinitely.

| Argument | Description | Default |
|----------|-------------|---------|
| `name` | The `name` argument is required and is used to determine which command is being used. | Required |
| `aliases` | The `aliases` argument is optional and is used to specify any additional names that this command can be run with. | `[]` |
| `description` | The `description` argument is optional will be displayed as the help text in the default help output. | `None` |

The sub-command and its options/arguments are accessible via the `program.command` attribute.

**Note:** Since a sub-command is always accessed via the `program.command` attribute, non-alphanumeric characters in the name ***are not*** converted to underscores.

```python
program = Program()

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

#### `program.parse(argv)`

Parses the command line arguments and sets up the program for the rest of the execution.

| Argument | Description | Default |
|----------|-------------|---------|
| `argv` | The `argv` argument should be the raw command line arguments for the program (typically `sys.argv`). Bones assumes that the script name is the first raw argument. | Required |

Once parse runs, the program should be populated with the data supplied in the command-line arguments.

```python
program = Program()
program.argument('some-argument')
program.parse(sys.argv) # ['program.py', 'argument #1']

print(program.some_argument) # 'argument #1'
```

#### `program.help()`

Returns the auto-generated help text for the command. Each sub-command will have its own help text.

```python
program = Program()
program.option('--force', aliases=['-f'], description='forces something to happen')
program.option('--output', aliases=['--out', '-o'], description='the output file')
program.argument('some-argument', description='an argument for this program')
program.command('action', description='performs some action')

print(program.help())

# Outputs:
#
# usage: None [options] <some-argument> <command>
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
```
