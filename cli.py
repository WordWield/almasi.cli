# ==============================================================================
# CLI
# ==============================================================================
# PURPOSE:
# Interpret controller commands directly from public method signatures.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Controller and method selection, help and argument binding.
# Delegates: Command behavior to the selected controller.
# ==============================================================================

import argparse
import importlib
import inspect
import pkgutil
import sys


class Cli:

	# ======================================================================
	# PRIVATE METHODS
	# ======================================================================

	# Discover controller modules through the entry's Python package.
	# ----------------------------------------------------------------------
	def _get_controllers(self):
		package_name = 'root.controllers'
		if __package__:
			package_name = f'{__package__}.{package_name}'

		package     = importlib.import_module(package_name)
		controllers = {}

		for module in pkgutil.iter_modules(package.__path__):
			if not module.ispkg and not module.name.startswith('_'):
				name         = module.name
				class_name   = ''.join(part.capitalize() for part in name.split('_'))
				controller   = importlib.import_module(f'{package_name}.{name}')

				controllers[name] = getattr(controller, class_name)()

		return controllers

	# Derive command parameters and help from the actual bound methods.
	# ----------------------------------------------------------------------
	def _add_methods(self, parser, controller):
		commands = parser.add_subparsers(dest='_command', required=True)

		for name, method in inspect.getmembers(controller, inspect.ismethod):
			if not name.startswith('_'):
				description = inspect.getdoc(method)
				command     = commands.add_parser(name, help=description, description=description)

				for parameter in inspect.signature(method).parameters.values():
					if parameter.annotation == list[str]:
						command.add_argument(parameter.name, nargs=argparse.REMAINDER)
					else:
						command.add_argument(parameter.name, type=parameter.annotation)

	# Bind the selected controller method without interpreting its arguments.
	# ----------------------------------------------------------------------
	def _dispatch(self, arguments: list[str]):
		parser      = argparse.ArgumentParser(prog='almasi')
		commands    = parser.add_subparsers(dest='_controller', required=True)
		controllers = self._get_controllers()

		for name, controller in controllers.items():
			self._add_methods(commands.add_parser(name), controller)

		values     = vars(parser.parse_args(arguments))
		controller = controllers[values.pop('_controller')]
		method     = getattr(controller, values.pop('_command'))
		method(**values)


if __name__ == '__main__':
	Cli()._dispatch(sys.argv[1:])
