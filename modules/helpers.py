import os
import struct
import numpy as np

from generated.io import BinaryStream
from generated.array import Array
from modules.formats.shared import assign_versions


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def as_bytes(inst, version_info={}):
	"""helper that returns the bytes representation of a pyffi struct"""
	# we must make sure that pyffi arrays are not treated as a list although they are an instance of 'list'
	if isinstance(inst, np.ndarray):
		return inst.tobytes()
	if isinstance(inst, list) and not isinstance(inst, Array):
		return b"".join(as_bytes(c, version_info) for c in inst)
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	with BinaryStream() as stream:
		assign_versions(stream, version_info)
		inst.write(stream)
		return stream.getvalue()


def zstr(b):
	return b + b"\x00"
