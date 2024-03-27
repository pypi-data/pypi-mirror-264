import shutil
from pathlib import Path

def ptos(path: str | Path) -> str:
	"""
	Resolves a path into a string

	Args:
		path: The path to resolve to a string

	Returns:
		The resolved path is returned. The function only resolves the input to a string if the
		input is a path.
	"""
	return str(path.resolve()) if isinstance(path, Path) else path

def stop(path: str | Path) -> Path:
	"""
	Creates a path from a string

	Args:
		path: The string path

	Returns:
		The path created from the input string. The function only creates a path if the input is
		a string.
	"""
	return Path(path) if isinstance(path, str) else path

def ltos(list: list[None | str | Path]) -> list[str]:
	"""
	Creates a list of strings from path items

	Args:
		list: The list of path items

	Returns:
		A list of path items
	"""
	resolved = []
	for item in list:
		if item is None:
			continue
		resolved.append(ptos(item))
	return resolved

def ltop(list: list[None | str | Path]) -> list[Path]:
	"""
	Creates a list of paths from string path items

	Args:
		list: The list of string path items

	Returns:
		A list of path items
	"""
	resolved = []
	for item in list:
		if item is None:
			continue
		resolved.append(stop(item))
	return resolved

def fmt_tmpl(src: str | Path, dst: None | str | Path, *args) -> str:
	"""
	Opens a text file, formats the text inside with the specified string arguments, and optionally
	saves the formatted text to a destination text file

	Args:
		src: The path of the file to read
		dst: The path of the file to save the formatted text to
		args: The string format arguments

	Returns:
		The formatted text
	"""
	src = stop(src)
	dst = stop(dst)
	txt = src.read_text().format(*args)
	if dst is None:
		return txt
	ref = dst.read_text() if dst.exists() else None
	if txt != ref:
		dst.write_text(txt)
	return txt

def del_fitems(fitems: list[None | str | Path]):
	"""
	Deletes the file items within a list from the file system

	Args:
		fitems: The list of file items to delete
	"""
	for fitem in ltop(fitems):
		if not fitem.exists():
			continue
		elif fitem.is_dir():
			shutil.rmtree(fitem)
		else:
			fitem.unlink()