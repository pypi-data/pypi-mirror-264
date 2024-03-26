from flask import Blueprint



class Component(Blueprint):

	def __init__(self, name, url, module=None):
		if url is None:
			raise ValueError('Cannot create a component without specifying a url')
		super().__init__(name, module, url_prefix=url)

	def mount(self, component):
		if component.url_prefix is None:
			raise ValueError('Cannot mount component: URL is not set')
		return self.register_blueprint(component)
