from flask import render_template as render
from . template import Template



class Abstract:

	def __call__(self, *args, **kwargs):
		raise NotImplemented

	def instance(self):
		instance = Template.Object()
		for key, function in self.MAP.items():
			setattr(instance, key, function())
		return instance

	def render(self, instance=None):
		instance = instance or self.instance()
		return render(self.template.path, instance=instance)
