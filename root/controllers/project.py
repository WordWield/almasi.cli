# ==============================================================================
# PROJECT
# ==============================================================================
# PURPOSE:
# Expose the lifecycle of an independent Almasi project.
#
# RESPONSIBILITY BOUNDARIES:
# Owns: Project command names and arguments.
# Delegates: Project lifecycle and repository management to Almasi Hub.
# ==============================================================================

from almasi._libraries import _Libraries


class Project:
	'Run and manage independent projects.'

	# ======================================================================
	# PUBLIC METHODS
	# ======================================================================

	# Start the configured project with its ordinary Hub lifecycle.
	# ----------------------------------------------------------------------
	def run(self, project: str):
		'Run a project, creating its default App if missing.'
		_Libraries.run('hub', ['run', project])

	# Remove the project's repositories and workspace after confirmation.
	# ----------------------------------------------------------------------
	def delete(self, project: str):
		'Delete a project and its data after confirmation.'
		_Libraries.run('hub', ['delete', project])

	# Preserve the project while changing its name.
	# ----------------------------------------------------------------------
	def rename(self, project: str, name: str):
		'Rename a stopped project without discarding its data.'
		_Libraries.run('hub', ['rename', project, name])

	# Recreate the initial project from the current starters.
	# ----------------------------------------------------------------------
	def reset(self, project: str):
		'Restore a stopped project to defaults after confirmation.'
		_Libraries.run('hub', ['reset', project])
