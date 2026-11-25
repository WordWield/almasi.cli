# ==============================================================================
# CLI
# ==============================================================================
# PURPOSE:
# Interpret commands directly from the public methods of this class.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Command names, signatures, help and argument binding.
# Delegates: Library acquisition and execution to the installed Almasi loader.
# ==============================================================================

import argparse
import inspect
import sys

from almasi._libraries import _Libraries


class Cli:

	_TEST_ENTRY = 'root/test.py'

	# ======================================================================
	# PRIVATE METHODS
	# ======================================================================

	# Derive the entire command interface from public bound methods.
	# ----------------------------------------------------------------------
	def _dispatch(self, arguments: list[str]):
		parser   = argparse.ArgumentParser(prog='almasi')
		commands = parser.add_subparsers(dest='_command', required=True)

		for name, method in inspect.getmembers(self, inspect.ismethod):
			if not name.startswith('_'):
				description = inspect.getdoc(method)
				command     = commands.add_parser(name, help=description, description=description)

				for parameter in inspect.signature(method).parameters.values():
					if parameter.annotation == list[str]:
						command.add_argument(parameter.name, nargs=argparse.REMAINDER)
					else:
						command.add_argument(parameter.name, type=parameter.annotation)

		values = vars(parser.parse_args(arguments))
		method = getattr(self, values.pop('_command'))
		method(**values)

	# ======================================================================
	# PUBLIC METHODS
	# ======================================================================

	# Execute the selected library without interpreting its own arguments.
	# ----------------------------------------------------------------------
	def run(self, library: str, arguments: list[str]):
		'Run a library and forward its remaining arguments unchanged.'
		_Libraries.run(library, arguments)

	# Execute the standard test entry from the acquired library checkout.
	# ----------------------------------------------------------------------
	def test(self, library: str, arguments: list[str]):
		'Run a library test suite and forward its remaining arguments unchanged.'
		_Libraries.run(
			library,
			arguments,
			entry = self._TEST_ENTRY,
			cwd   = _Libraries.get_path(library)
		)


if __name__ == '__main__':
	Cli()._dispatch(sys.argv[1:])
