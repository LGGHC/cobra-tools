from generated.context import ContextReference


class AuxEntry:

	"""
	describes an external AUX resource
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into files list
		self.file_index = 0

		# maybe index into extension list
		self.extension_index = 0

		# byte count of the complete external resource file
		self.size = 0
		self.set_defaults()

	def set_defaults(self):
		self.file_index = 0
		self.extension_index = 0
		self.size = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.file_index = stream.read_uint()
		self.extension_index = stream.read_uint()
		self.size = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.file_index)
		stream.write_uint(self.extension_index)
		stream.write_uint(self.size)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'AuxEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_index = {self.file_index.__repr__()}'
		s += f'\n	* extension_index = {self.extension_index.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
