# ==============================================================================
# LIBRARY
# ==============================================================================
# PURPOSE:
# Execute independently acquired Almasi libraries and their tests.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Library command semantics and selection of the test entry.
# Delegates: Acquisition and process replacement to the installed loader.
# ==============================================================================

from almasi._libraries import _Libraries


class Library:
	'Run and test Almasi libraries.'

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
