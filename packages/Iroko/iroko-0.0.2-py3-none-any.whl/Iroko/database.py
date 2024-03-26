import string
import pathlib
import sqlite3

from . yaml import YAML



class Database:

	def __init__(self, schema, path=None, reset=False):
		self.schema = YAML.read(schema)
		path = path or ':memory:'
		self.connection = sqlite3.connect(path)
		self.initialize()

	def initialize(self):
		cursor = self.connection.cursor()
		template = {}
		for template_key, template_value in self.schema['template']['table'].items():
			template[template_key] = string.Template(template_value)

		for template_key, tables in self.schema['table'].items():
			for table, structure in tables.items():
				command = template[template_key].substitute({'table': table, 'structure': structure})
				try:
					cursor.execute(command)
				except sqlite3.OperationalError as exception:
					args = (*exception.args, command)
					exception.args = args
					raise
