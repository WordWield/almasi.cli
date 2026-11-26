# ==============================================================================
# PROJECT
# ==============================================================================
# PURPOSE:
# Expose named project lifecycle operations on the local command line.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Project command signatures and argument forwarding.
# Delegates: Project lifecycle to Hub through the existing library launcher.
# ==============================================================================

from almasi._libraries import _Libraries


class Project:

	# ======================================================================
	# PUBLIC METHODS
	# ======================================================================

	# Run the project in Hub's standalone application context.
	# ----------------------------------------------------------------------
	def run(self, project: str, user: str):
		'Create or run a named project.'
		_Libraries.run('hub', ['run', user, project])

	# Permanently remove the stopped project's repositories and local workspace.
	# ----------------------------------------------------------------------
	def delete(self, project: str, user: str):
		'Permanently delete a project. Stop Hub, App and all Sources first.'
		_Libraries.run('hub', ['delete', user, project])

	# Move a stopped project without replacing its repositories or ontology.
	# ----------------------------------------------------------------------
	def rename(self, project: str, user: str, new_name: str):
		'Rename a project. Stop Hub, App and all Sources first.'
		_Libraries.run('hub', ['rename', user, project, new_name])
