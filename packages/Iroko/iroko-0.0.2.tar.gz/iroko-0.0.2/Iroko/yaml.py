import yaml



class YAML:

	@classmethod
	def read(self, path):
		with open(path, 'r') as file:
			return yaml.load(file, Loader=yaml.CSafeLoader)

	@classmethod
	def write(self, path, data):
		with open(path, 'w') as file:
			yaml.dump(data, file, Dumper=yaml.CSafeDumper, default_flow_style=False)
