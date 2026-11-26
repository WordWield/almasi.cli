# Almasi CLI

The dynamically acquired command interface of [Almasi](https://github.com/WordWield/almasi).
The loader acquires and updates this library before executing its entry.

```sh
almasi <controller> <method> <args>
almasi --help
almasi library --help
almasi project --help
```

Each public module in `root/controllers/` exposes the corresponding PascalCase
controller class. Its public bound methods define command names, positional
parameters and help. Scalar parameters use their annotations; a final
`list[str]` parameter receives the remaining arguments unchanged.
Method and class docstrings supply help. Private methods are never commands.
Adding a controller or method requires no dispatcher changes.

## Library

```sh
almasi library run hub --help
almasi library test o
```

Run executes the ordinary library entry and preserves the caller's working
directory. Test executes `root/test.py` from the acquired library checkout.
Both delegate acquisition, dependency installation and process replacement
to the loader. A missing entry fails; the script determines the exit status.

## Project

```sh
almasi project run demo
almasi project rename demo example
almasi project reset example
almasi project delete example
```

These operations acquire and execute Hub. Configure the project owner,
client and scoped credential as described in the matching
[Hub documentation](https://github.com/WordWield/almasi.hub).
Stop Hub before rename, reset or delete. Reset and delete are destructive
and require confirmation. Project run creates the default App if missing.

This interface replaces the former top-level `run` and `test` commands.
The loader's `almasi --version` remains an offline installer diagnostic.
The CLI is trusted executable code acquired by the ordinary Git policy.
