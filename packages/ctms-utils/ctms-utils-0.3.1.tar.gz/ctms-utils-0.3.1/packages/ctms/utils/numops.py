def u8(value: int) -> int:
	"""
	Returns a 1 byte unsigned integer representation of a number

	Args:
		value: The number to convert to a 1 byte unsigned integer representation

	Returns:
		The 1 byte unsigned integer representation of the input number
	"""
	return value & 0xFF

def u16(value: int) -> int:
	"""
	Returns a 2 byte unsigned integer representation of a number

	Args:
		value: The number to convert to a 2 byte unsigned integer representation

	Returns:
		The 2 byte unsigned integer representation of the input number
	"""
	return value & 0xFFFF

def u32(value: int) -> int:
	"""
	Returns a 4 byte unsigned integer representation of a number

	Args:
		value: The number to convert to a 4 byte unsigned integer representation

	Returns:
		The 4 byte unsigned integer representation of the input number
	"""
	return value & 0xFFFFFFFF

def align(value: int, alignment: int) -> int:
	"""
	Gets an aligned integer value from a specified integer

	Args:
		value:     The integer value to get the aligned value of
		alignment: The alignment value

	Returns:
		The aligned integer value
	"""
	if (alignment == 0) or ((rem := (value % alignment)) == 0):
		return value
	return value + alignment - rem

def parse_hex(txt: str) -> None | int:
	"""
	Parses a hex string into an integer

	Args:
		The hex string to parse

	Returns:
		The integer parsed from the hex string if successful, otherwise None
	"""
	return parse(txt, 16)

def parse(txt: str, base: int = 10) -> None | int:
	"""
	Parses a string into an integer using the specified base

	Args:
		txt: The string to parse
		base: The number base of the string

	Returns:
		The integer parsed from the string if successful, otherwise None
	"""
	try:
		return int(txt, base)
	except:
		return None