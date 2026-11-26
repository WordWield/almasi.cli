# ==============================================================================
# PROJECT
# ==============================================================================
# PURPOSE:
# Declare the project commands before their Hub implementation.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Project command signatures and unavailable-operation diagnostics.
# Delegates: Future project lifecycle operations to Hub.
# ==============================================================================

import sys


class Project:

	# ======================================================================
	# PUBLIC METHODS
	# ======================================================================

	# Reserve the CLI contract without changing project state.
	# ----------------------------------------------------------------------
	def run(self, project: str):
		'Start a named project. Not implemented yet.'
		sys.exit('project run: not implemented')

	# Reserve the CLI contract without changing project state.
	# ----------------------------------------------------------------------
	def delete(self, project: str):
		'Delete a named project. Not implemented yet.'
		sys.exit('project delete: not implemented')

	# Reserve the CLI contract without changing project state.
	# ----------------------------------------------------------------------
	def rename(self, project: str, new_name: str):
		'Rename a named project. Not implemented yet.'
		sys.exit('project rename: not implemented')

	# Reserve the CLI contract without changing project state.
	# ----------------------------------------------------------------------
	def reset(self, project: str):
		'Restore a named project to its defaults. Not implemented yet.'
		sys.exit('project reset: not implemented')
