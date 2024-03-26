import math
import uuid



class Scheme:


	class Parity:

		def __init__(self, scheme):
			self.scheme = scheme

			r = range(int(math.log2(scheme.LENGTH)) + 1)
			self.INDEX = tuple([((2 ** i) - 1) for i in r])
			self.MASK  = tuple([(1 << _) for _ in self.INDEX])
			self.GROUP = tuple([self.group(_) for _ in self.INDEX])

		def group(self, position):
			b = 0

			for i in range(self.scheme.LENGTH):
				if (position + 1) & (i + 1) and (position != i):
					b |= 1 << (i)

			return b


	def __init__(self, length):
		self.LENGTH = length
		self.MASK = (1 << length) - 1
		self.PARITY = Scheme.Parity(self)



SCHEME128 = Scheme(128)



class Identifier:


	SCHEME = SCHEME128


	@classmethod
	def random(self):
		n = 0

		LENGTH_UUID = 64
		for i in range(max(1, self.SCHEME.LENGTH // LENGTH_UUID)):
			code = uuid.uuid4().int
			n ^= (code << (8 * i))

		n = n & self.SCHEME.MASK
		return (n)


	def __init__(self, value=None, debug=False):
		self.value = self.random() if value is None else value
		if value is None:
			self.encode()
		else:
			if not debug:
				self.correct()


	def encode(self):
		correction = 0

		for (index, position, parity, count) in self.parity():
			if (count + parity) & 1:
				continue
			else:
				correction |= (1 << position)

		self.value = correction ^ self.value

	def parity(self):
		value = self.value
		for index, position in enumerate(self.SCHEME.PARITY.INDEX):
			parity = (value & (1 << position)) >> position
			group  = value & self.SCHEME.PARITY.GROUP[index]
			count  = self.count(group)
			yield (index, position, parity, count)

	def count(self, value):
		# @TODO:
		# Can be optimized more
		n = 0
		for _ in range(self.SCHEME.LENGTH):
			if (1 << _) & value:
				n += 1
		return n

	def correct(self):
		error_index = self.error_detect()
		if error_index is None:
			return
		self.error_correct(error_index)

	def error_detect(self):
		position_error = 0

		for (index, position, parity, count) in self.parity():
			if not ((count + parity) & 1):
				position_error |= 1 << index

		return None if position_error == 0 else (position_error - 1)

	def error_correct(self, position):
		self.value = self.value ^ (1 << position)


	def __int__(self):
		return self.value

	def __eq__(self, other):
		return other.value == self.value

	def __str__(self):
		return f'{self.value:032X}'

	def __repr__(self):
		return f'Identifier({self.value:032X})'
