# Almasi CLI

The dynamically acquired command interface of [Almasi](https://github.com/WordWield/almasi).
The loader acquires and updates this library before executing its entry.

```sh
almasi <controller> <method> <args>
almasi library run hub run apodgorny demo
almasi project run apodgorny demo
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

The project controller forwards the following commands to the standalone Hub
entry, where the Project service owns their implementation:

```sh
almasi project run <user> <project>
almasi project delete <user> <project>
almasi project rename <user> <project> <new_name>
```

Delete permanently removes the cloud repositories and local workspace including
ontology. Rename preserves repository history and local state. The caller must
stop Hub, App and all Sources before either operation; no stopped-state check
is performed. There is no reset operation. Use the coordinated Hub update and
read its [Project API](https://github.com/WordWield/almasi.hub/blob/master/docs/project.md).

The previous flat `almasi run` and `almasi test` commands are now
`almasi library run` and `almasi library test`.

The loader's `almasi --version` remains an offline installer diagnostic.
The CLI is trusted executable code acquired using the same Git policy
as any other Almasi library.
