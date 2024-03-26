import colorsys



'''
This library is designed to only
deal with 8-bit color.
'''



class Color:


	@classmethod
	def RGB(self, r, g, b):
		limit = range(256)
		try:
			assert r in limit
			assert g in limit
			assert b in limit
		except AssertionError:
			raise ValueError(f'RGB values must all lie in the range of 0 <= r, g, b <= 255', r, g, b)

		color = self()
		color.channel.extend([r, g, b])


	@classmethod
	def Hex(self, code):
		try:
			test = code + 1
		except TypeError:
			return self.HexString(code)
		else:
			return self.HexLiteral(code)

	@classmethod
	def HexLiteral(self, code):
		values = []
		for _ in range(3):
			values.insert(0, [0xFF & code])
			code = code >> 8

		color = self()
		color.channel.extend(values)
		return color

	@classmethod
	def HexString(self, code):
		code = code.removeprefix('#')
		length = len(code)
		if length not in (6, ):
			# @TODO:
			# Add support for hex codes with length of 3
			raise ValueError(f'Invalid size for hex code: {length}', f'#{code}')

		values = [int(source[i:i+2], 16) for i in range(0, 6, 2)]
		color = self()
		color.channel.extend(values)
		return color

	def __init__(self, *args, **kwargs):
		self.channel = []

	def __bytes__(self):
		return bytes(self.channel)

	def __iter__(self):
		return iter(self.channel)

	@classmethod
	def Scale(self, color, factor):
		hls = list(colorsys.rgb_to_hls(*color))
		hls[1] = hls[1] * factor
		rbg = colorsys.hls_to_rgb(*hls)
		values = [int(_) for _ in rgb]
		color = self()
		color.channel.extend(values)
		return color
