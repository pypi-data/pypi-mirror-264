from typing import overload

from . import(
	clib,
	numops
)

def extend_to(data: bytes | bytearray, dlen: int, pad: int = 0xFF) -> bytes | bytearray:
	"""
	Extends a buffer to a specified length. If the length value is less than or equal to the length
	of the buffer, no operation is performed.

	Args:
		data: The buffer to extend
		dlen: The length to extend the buffer to
		pad:  The byte value of the bytes to append to the buffer

	Returns:
		The original buffer is returned
	"""
	if (extra := (dlen - len(data))) > 0:
		data.extend((pad & 0xFF).to_bytes() * extra)
	return data

def rev16(data: bytes | bytearray, pad: int = 0xFF) -> bytearray:
	"""
	Creates a new 2 byte aligned bytearray from the data within a buffer and reverses the endianness
	of all 2 byte words within the buffer

	Args:
		data: The buffer containing the data to reverse
		pad:  The padding value for bytes appended to the buffer if it is extended

	Returns:
		A new reversed bytearray
	"""
	dlen = numops.align(len(data), 2)
	data = extend_to(bytearray(data), dlen, pad)
	clib.rev16(clib.to_ptr(data), dlen)
	return data

def crc32(data: bytes | bytearray) -> int:
	"""
	Calculates a crc32 of a buffer

	Args:
		data: The buffer containing the data to calculate the crc32 of

	Returns:
		The crc32 calculated from the data within the input buffer
	"""
	return numops.u32(clib.crc32(clib.to_ptr(data), len(data)))

def utob8le(value: int) -> bytes:
	"""
	Encodes an integer to a 1 byte little endian representation

	Args:
		value: The integer value to encode

	Returns:
		A bytes object representing the encoded integer is returned
	"""
	return numops.u8(value).to_bytes(1, 'little', signed=False)

def utob16le(value: int) -> bytes:
	"""
	Encodes an integer to a 2 byte little endian representation

	Args:
		value: The integer value to encode

	Returns:
		A bytes object representing the encoded integer is returned
	"""
	return numops.u16(value).to_bytes(2, 'little', signed=False)

def utob32le(value: int) -> bytes:
	"""
	Encodes an integer to a 4 byte little endian representation

	Args:
		value: The integer value to encode

	Returns:
		A bytes object representing the encoded integer is returned
	"""
	return numops.u32(value).to_bytes(4, 'little', signed=False)

def utob64le(value: int) -> bytes:
	"""
	Encodes an integer to an 8 byte little endian representation

	Args:
		value: The integer value to encode

	Returns:
		A bytes object representing the encoded integer is returned
	"""
	return value.to_bytes(8, 'little', signed=False)

def create(dlen: int, fill = 0xFF) -> bytearray:
	"""
	Creates a new bytearray with all bytes initialized to a fill value

	Args:
		dlen: The length of the bytearray to create
		fill: The fill value for each byte of the array
	"""
	return bytearray(utob8le(fill)) * dlen

def slice(data: bytes | bytearray, offset: int, clen: int) -> bytes | bytearray:
	"""
	Slices a data buffer

	Args:
		data:   The data buffer to slice
		offset: The offset into the buffer to slice from
		clen:   The number of bytes to include in the slice

	Returns:
		A data buffer consisting of the sliced data
	"""
	return data[offset:offset+clen]

def write(dst: bytearray, offset: int, src: bytes | bytearray) -> None:
	"""
	Writes source data into a destination data buffer

	Args:
		dst:    The destination data buffer to write to
		offset: The offset into the destination data buffer
		src:    The source buffer containing the data to write
	"""
	dst[offset:offset+len(src)] = src