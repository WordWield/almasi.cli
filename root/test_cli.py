# ==============================================================================
# TEST CLI
# ==============================================================================
# PURPOSE:
# Verify that the public class API is the only source of CLI commands.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Command binding and dispatch assertions.
# Delegates: Actual library acquisition and execution to loader tests.
# ==============================================================================

import io
import unittest

from contextlib    import redirect_stdout, redirect_stderr
from unittest.mock import Mock, patch

from almasi                              import cli
from almasi._libraries                   import _Libraries
from almasi.cli.root.controllers.library import Library


_sample = Mock()


# Supply an additional public method without changing the dispatcher.
# ----------------------------------------------------------------------
def sample(self, name: str, arguments: list[str]):
	_sample(name=name, arguments=arguments)


class TestCli(unittest.TestCase):

	# ======================================================================
	# PUBLIC METHODS
	# ======================================================================

	# Bind names and preserve downstream flags and argument boundaries.
	# ----------------------------------------------------------------------
	def test_run(self):
		with patch.object(_Libraries, 'run') as run:
			cli.Cli()._dispatch(['library', 'run', 'hub', 'demo', 'Word Wield', '--flag'])
			run.assert_called_once_with('hub', ['demo', 'Word Wield', '--flag'])

	# Test execution must use the library's existing test entry.
	# ----------------------------------------------------------------------
	def test_test(self):
		with patch.object(_Libraries, 'run') as run:
			cli.Cli()._dispatch(['library', 'test', 'o'])
			run.assert_called_once_with('o', [], entry='root/test.py', cwd=_Libraries.get_path('o'))

	# New public methods automatically become commands with named binding.
	# ----------------------------------------------------------------------
	def test_public_api(self):
		_sample.reset_mock()

		with patch.object(Library, 'sample', sample, create=True):
			cli.Cli()._dispatch(['library', 'sample', 'value', '--flag'])

		_sample.assert_called_once_with(name='value', arguments=['--flag'])

	# Reject private methods before invoking any command.
	# ----------------------------------------------------------------------
	def test_private_api(self):
		with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
			cli.Cli()._dispatch(['library', '_dispatch'])

		self.assertEqual(error.exception.code, 2)

	# Derive help from the same public methods used for execution.
	# ----------------------------------------------------------------------
	def test_help(self):
		output = io.StringIO()

		with redirect_stdout(output), self.assertRaises(SystemExit) as error:
			cli.Cli()._dispatch(['--help'])

		self.assertEqual(error.exception.code, 0)
		self.assertIn('{library,project}', output.getvalue())

	# Discover project operations without invoking any lifecycle mechanism.
	# ----------------------------------------------------------------------
	def test_project_help(self):
		output = io.StringIO()

		with redirect_stdout(output), self.assertRaises(SystemExit) as error:
			cli.Cli()._dispatch(['project', '--help'])

		self.assertEqual(error.exception.code, 0)
		self.assertIn('{delete,rename,run}', output.getvalue())

	# Forward project identity and lifecycle command unchanged to Hub.
	# ----------------------------------------------------------------------
	def test_project_commands(self):
		commands = [
			['run', 'alice', 'demo'],
			['delete', 'alice', 'demo'],
			['rename', 'alice', 'demo', 'next']
		]

		with patch.object(_Libraries, 'run') as run:
			for arguments in commands:
				with self.subTest(arguments=arguments):
					run.reset_mock()
					cli.Cli()._dispatch(['project', *arguments])
					run.assert_called_once_with('hub', arguments)

	# Reset is not part of the project lifecycle API.
	# ----------------------------------------------------------------------
	def test_project_reset_is_absent(self):
		with patch.object(_Libraries, 'run') as run, \
			redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
			cli.Cli()._dispatch(['project', 'reset', 'alice', 'demo'])

		self.assertEqual(error.exception.code, 2)
		run.assert_not_called()
