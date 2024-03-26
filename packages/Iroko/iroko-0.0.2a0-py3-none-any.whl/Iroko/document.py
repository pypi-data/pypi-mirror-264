import textwrap



class Block:

	def __init__(self, source, level=0):
		self.nodes = []
		self.level = level
		self.parse_subblock_section(source)
		self.parse_subblock_content(source)

	def parse_subblock_section(self, source):
		try:
			source = source['.section']
		except KeyError:
			return
		else:
			self.heading = source['heading']

	def parse_subblock_content(self, source):
		try:
			source = source['.content']
		except KeyError:
			return
		else:
			for element in source:
				block = Block(element, level=self.level + 1)
				self.nodes.append(block)

	def __iter__(self):
		return iter(self.nodes)

	def __str__(self):
		try:
			heading = f' - ({self.heading})'
		except AttributeError:
			heading = ''

		info = f'[{self.level} / {len(self.nodes)} nodes]'
		return f'Block {info}{heading}'

	def print_tree(self):
		text = textwrap.indent(str(self), '    ' * self.level)
		print(text)
		for _ in self:
			_.print_tree()



class Document:

	Block = Block

	def __init__(self, type, root=None):
		self.type = type
		self.root = root
