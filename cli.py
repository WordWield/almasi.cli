# ==============================================================================
# CLI
# ==============================================================================
# PURPOSE:
# Interpret commands directly from controller classes and their public methods.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Controller discovery, help and argument binding.
# Delegates: Each operation to its controller.
# ==============================================================================

import argparse
import importlib
import inspect
import os
import pkgutil
import sys


class Cli:

	# ======================================================================
	# PRIVATE METHODS
	# ======================================================================

	# Discover controller modules beside this entry, without a command registry.
	# ----------------------------------------------------------------------
	def _get_controllers(self):
		directory   = os.path.join(os.path.dirname(__file__), 'root', 'controllers')
		package     = f'{__package__}.root.controllers' if __package__ else 'root.controllers'
		controllers = {}

		for module in pkgutil.iter_modules([directory]):
			if not module.ispkg and not module.name.startswith('_'):
				implementation = importlib.import_module(f'{package}.{module.name}')
				class_name     = ''.join(part.capitalize() for part in module.name.split('_'))
				controllers[module.name] = getattr(implementation, class_name)()

		return controllers

	# Derive each method's arguments and help from its public signature.
	# ----------------------------------------------------------------------
	def _add_methods(self, parser, controller):
		commands = parser.add_subparsers(dest='_method', required=True)

		for name, method in inspect.getmembers(controller, inspect.ismethod):
			if not name.startswith('_'):
				description = inspect.getdoc(method)
				command     = commands.add_parser(name, help=description, description=description)

				for parameter in inspect.signature(method).parameters.values():
					if parameter.annotation == list[str]:
						command.add_argument(parameter.name, nargs=argparse.REMAINDER)
					else:
						command.add_argument(parameter.name, type=parameter.annotation)

	# Bind the selected controller and method before invoking domain behavior.
	# ----------------------------------------------------------------------
	def _dispatch(self, arguments: list[str]):
		parser      = argparse.ArgumentParser(prog='almasi')
		commands    = parser.add_subparsers(dest='_controller', required=True)
		controllers = self._get_controllers()

		for name, controller in controllers.items():
			description = inspect.getdoc(type(controller))
			command     = commands.add_parser(name, help=description, description=description)
			self._add_methods(command, controller)

		values     = vars(parser.parse_args(arguments))
		controller = controllers[values.pop('_controller')]
		method     = getattr(controller, values.pop('_method'))
		method(**values)


if __name__ == '__main__':
	Cli()._dispatch(sys.argv[1:])
