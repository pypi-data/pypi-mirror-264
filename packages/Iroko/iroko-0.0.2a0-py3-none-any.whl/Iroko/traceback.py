import sys
import click
import pathlib
import textwrap
import functools
import traceback



class Formatter:

	def __init__(self, instance):
		self.instance = instance

	def code(self):
		value = textwrap.indent(self.instance.code, prefix='\n\t')
		color = (255, 255, 255)
		return click.style(value, fg=color)

	def path(self):
		value = self.instance.path
		color = (10, 230, 255)
		return click.style(value, fg=color)

	def filepath(self):
		value = self.instance.path.parent
		color = (66, 188, 229)
		return click.style(f'-- {value}', fg=color, bold=True)

	def file(self):
		value = self.instance.path.name
		color = (255, 180, 40)
		return click.style(value, fg=color)

	def function(self):
		value = self.instance.function
		return value

	def line(self):
		value = self.instance.line
		color = (230, 180, 40)
		return click.style(value, fg=color, bold=True)

	def package(self):
		value = self.instance.package
		color = (200, 80, 80)
		return click.style(value, fg=color, bold=True)

	def location(self):
		file = self.file()
		line = self.line()

		return f'{file}:{line}'

	def __str__(self):
		# header = f'{self.package()} / {self.file()}:{self.line()}'
		# return f'{header}\n  {self.path()}{code}\n'
		code = textwrap.indent(self.code(), '\t')

		header = f'{self.location()}'
		return f'{self.filepath()}\n\t{header}\n\t{self.function()}{code}\n'



class Frame:

	def __init__(self, traceback, instance, formatter=None, position=None):
		self.instance = instance
		self.traceback = traceback

		self.position = position

		formatter = formatter if formatter is not None else Formatter
		self.formatter = formatter(self)

	@property
	def function(self):
		function = self.instance.name
		return f'{function}()' if function != '<module>' else function

	@property
	def code(self):
		return self.instance.line

	@property
	def path(self):
		path = pathlib.Path(self.instance.filename)

		try:
			path = path.relative_to(self.traceback.Path.PACKAGE)
		except ValueError:
			pass

		try:
			path = path.relative_to(self.traceback.Path.ENVIRONMENT)
		except ValueError:
			pass

		return path

	@property
	def line(self):
		return self.instance.lineno

	@property
	def package(self):
		try:
			path = pathlib.Path(self.instance.filename)
			path = path.relative_to(self.traceback.Path.PACKAGE)
			return self.traceback.PACKAGE
		except ValueError:
			return self.path.parts[0]

	def __str__(self):
		return str(self.formatter)



class Traceback:

	@classmethod
	def Show(self, base):
		exc_type, exc_value, exc_traceback = sys.exc_info()
		stack = traceback.extract_tb(exc_traceback)
		instance = self(base, stack)
		instance.print()
		self.ShowException(exc_type, exc_value)
		sys.exit(1)

	@classmethod
	def ShowException(self, exc_type, exc_value):
		click.echo('----------------\n')
		exc_name    = click.style(f'{exc_type.__name__}', bold=True)
		exc_message = click.style(f'{exc_value}', bold=False)
		click.echo(f'{exc_name}\n\t{exc_message}\n')

	def __init__(self, base, stack):
		self.stack = stack
		# print(self.stack, dir(self.stack))

		class Path:
			BASE = base
			MODULE = pathlib.Path(BASE)
			PACKAGE = MODULE.parent
			ENVIRONMENT = PACKAGE.parent

		self.Path = Path
		self.PACKAGE = Path.PACKAGE.name

	def __len__(self):
		return len(self.stack)

	def __iter__(self):
		stack = self.stack

		size = len(self.stack)
		index = range(size)

		iterator = zip(stack, index)
		for frame, weight in iterator:
			yield Frame(self, frame, position=(weight, size))

	def print(self):
		for frame in self:
			print(frame)
