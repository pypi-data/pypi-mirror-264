import subprocess
from pathlib import Path
from . import futils

def get_commit(dir: None | str | Path = None) -> None | str:
	"""
	Gets the current GIT commit hash for a given directory

	Args:
		The directory to retrieve the current GIT commit hash of

	Returns:
		If successful, the commit hash is returned, otherwise None is returned
	"""
	result = subprocess.run(['git', 'rev-parse', 'HEAD'],
		cwd=futils.ptos(dir), capture_output=True)
	return result.stdout.decode().strip() if result.returncode == 0 else None