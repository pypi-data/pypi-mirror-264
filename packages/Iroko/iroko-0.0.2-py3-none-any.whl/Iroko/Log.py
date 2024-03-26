import sys
import click
import pathlib
import logging
import textwrap



class Formatter:

	class Abstract(logging.Formatter):
		pass

	class Console(Abstract):

		class Color:
			INFO = 42
			ERROR = 9
			DEBUG = 166
			WARNING = 220
			CRITICAL = 9

			BODY = 15
			# PATH = 68
			PATH = 189
			LINE = 15
			# FUNCTION = 104
			FUNCTION = 69

		def path(self, record):
			path = pathlib.Path(record.pathname)
			for i, element in enumerate(path.parts):
				if element == 'site-packages':
					break

			path = pathlib.Path(*path.parts[i+1:])
			return click.style(path, fg=self.Color.PATH)

		def level(self, record):
			level = click.style(record.levelname, fg=getattr(self.Color, record.levelname), bold=False)
			return level

		def location(self, record):
			path = self.path(record)
			fn = click.style(record.funcName, fg=self.Color.FUNCTION)
			line = click.style(record.lineno, fg=self.Color.LINE, bold=True)
			return f'{path}:{line} {fn}'

		def body(self, record):
			message = textwrap.indent(record.msg, prefix='\t')
			return click.style(message, fg=self.Color.BODY)

		def name(self, record):
			return click.style(f'{record.name}', fg=self.Color.BODY)

		def format(self, record):
			name = self.name(record)
			body = self.body(record)
			level = self.level(record)
			location = self.location(record)
			return f'── {level} [{name}] ────────\n   {location}\n\n{body}'



def Get(name, level):
	log = logging.getLogger(name)
	handler = logging.StreamHandler(sys.stderr)
	formatter = Formatter.Console()
	handler.setFormatter(formatter)
	log.addHandler(handler)
	log.setLevel(level)
	return log
