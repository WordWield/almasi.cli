# Almasi CLI

The dynamically acquired command interface of [Almasi](https://github.com/WordWield/almasi).
The loader acquires and updates this library before executing its entry.

```sh
almasi <controller> <method> <args>
almasi library run hub demo apodgorny
almasi library test o
almasi library run hub --help
almasi project --help
```

Controller modules live under `root/controllers/`. A module's snake_case
filename defines its controller name; it contains a corresponding PascalCase
class with a parameterless constructor. Python package discovery finds these
modules automatically. Public bound methods define commands, method docstrings
supply help, scalar annotations define positional argument types, and a final
`list[str]` parameter receives remaining arguments unchanged. Private methods
are not exposed.

The library controller preserves existing execution behavior: run executes the
selected library's standalone entry from the caller's directory; test executes
`root/test.py` from that library's checkout. Both delegate acquisition,
dependency installation and process replacement to the loader. Neither returns
on successful execution.

The project controller declares `run <project>`, `delete <project>`,
`rename <project> <new_name>`, and `reset <project>`. All four exit with an
explicit not-implemented error and make no changes. Their lifecycle behavior
will be implemented by Hub.

The previous flat `almasi run` and `almasi test` commands are now
`almasi library run` and `almasi library test`.

The loader's `almasi --version` remains an offline installer diagnostic.
The CLI is trusted executable code acquired using the same Git policy
as any other Almasi library.
