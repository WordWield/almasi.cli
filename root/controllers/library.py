# ==============================================================================
# LIBRARY
# ==============================================================================
# PURPOSE:
# Expose the existing library execution operations to the CLI.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Library command signatures and test entry selection.
# Delegates: Acquisition and execution to the installed Almasi loader.
# ==============================================================================

from almasi._libraries import _Libraries


class Library:

	_TEST_ENTRY = 'root/test.py'

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
