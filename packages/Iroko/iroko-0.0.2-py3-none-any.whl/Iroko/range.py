import bisect



'''

--- [0 - 100] --- [150 - 180] --- [240 - 900] ---

'''



class Element:

	def __init__(self, start, end):
		self.start = start
		self.end = end

	def __str__(self):
		return f'Range {self.start} ... {self.end}'



class Range:

	def __init__(self):
		self.elements = []

	def extents(self):
		try:
			return Element(self.elements[0].start, self.elements[-1].end)
		except IndexError:
			return None

	def __contains__(self, key):
		return False

	def __iter__(self):
		for element in self.elements:
			for _ in range(element.start, element.end):
				yield _

	def insert_element(self, element):
		# not considering overlapping ranges yet
		index = bisect.bisect_left(self.storage, element, key=lambda x: x.end)
		self.storage.insert(index, element)

	def gaps(self):
		if len(self.storage) <= 1:
			return

		for a, b in zip(self.storage[:-1], self.storage[1:]):
			yield (a, b)
