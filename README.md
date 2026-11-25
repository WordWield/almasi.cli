# Almasi CLI

The dynamically acquired command interface of [Almasi](https://github.com/WordWield/almasi).
The loader acquires and updates this library before executing its entry.
No separate CLI installation or registry is necessary.

The public methods of `Cli` in [cli.py](cli.py) are the sole source of command
names, parameter names and help. Run `almasi --help` for the live command
interface. Required scalar parameters are positional on the command line and
bound by name when calling the method; a final `list[str]` parameter receives
the remaining arguments unchanged. The current methods accept a library's
canonical snake_case name and its remaining string arguments. Method
docstrings supply command help. Private methods are never commands.

The run operation uses the selected library's ordinary standalone entry
and preserves the caller's working directory. The test operation executes
the library's existing `root/test.py` from its checkout directory. Both
delegate acquisition, dependency installation and process replacement to
the loader. Neither returns on successful execution; the executed script
determines the exit status. A library without the required entry fails.

Examples (requires the loader supporting dynamic CLI dispatch):

```sh
almasi run hub demo apodgorny
almasi test o
almasi run hub --help
```

The loader's `almasi --version` remains an offline installer diagnostic.
The CLI is trusted executable code acquired using the same Git policy
as any other Almasi library.
