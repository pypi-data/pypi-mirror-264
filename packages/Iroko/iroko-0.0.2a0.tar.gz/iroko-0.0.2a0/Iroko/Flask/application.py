import os
import enum
import flask
import pathlib



class Environment:

	class Path:

		def __init__(self, environment, module):
			self.environment = environment

			self.module = pathlib.Path(module)
			self.package = self.module.parent

			self.root = pathlib.Path('.').resolve()
			self.template = self.package / 'template'


	class MODE(str, enum.Enum):
		PRODUCTION = 'production'
		DEVELOPMENT = 'development'


	def __init__(self, application, module):
		self.application = application
		self.path = self.Path(self, module)
		self.resolve_mode()

	def resolve_mode(self):
		key = self.application.NAME.upper()
		mode = os.getenv(f'{key}_MODE', 'production').lower()
		self.mode = Environment.MODE(mode)



class Application:

	NAME = None
	'''
	NAME is used to create a prefix for environment variables
	'''

	Controller = flask.Flask

	def __init__(self, module):
		self.validate_application_name()

		self.environment = Environment(self, module)
		self.instance = self.controller()

	def validate_application_name(self):
		name = self.NAME
		if name is None:
			raise RuntimeError(f'{type(self).__name__} does not have a valid name')

		# @TODO
		# More validation to ensure that NAME can be used
		# as a prefix for environment variables


	def controller(self):
		environment = self.environment
		kwargs = {}

		mode = environment.mode
		if mode is Environment.MODE.PRODUCTION:
			pass

		elif mode is Environment.MODE.DEVELOPMENT:
			kwargs['static_folder'] = environment.path.root / static

		# super().__init__(
		# 	static_url_path='/static'
		# )

		return self.Controller(
			self.NAME,
			template_folder=environment.path.template,
			**kwargs
		)


	def mount(self, *components):
		for component in components:
			self.instance.register_blueprint(component)

	def run(self):
		debug = (self.environment.mode == Environment.MODE.DEVELOPMENT)
		return self.instance.run(debug=debug)
