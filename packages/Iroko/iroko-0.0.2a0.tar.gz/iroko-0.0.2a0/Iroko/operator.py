import click



class Operator:


	class Format:

		# @TODO:
		# Implementation pending

		class Binary:

			def fbl(number, length):
				return format(number, f'0{length}b')

			b = lambda n: fbl(n, 128)

		class Hex:
			pass


	@staticmethod
	def Print(instance, *args, **kwargs):
		try:
			fn = instance.__print__
		except AttributeError:
			return print(instance)

		output = fn(*args, **kwargs)
		if output is None:
			return

		click.echo(output)


	@staticmethod
	def Inspect(instance, *args, **kwargs):
		try:
			fn = instance.__inspect__
		except AttributeError:
			print(instance)
			return

		output = fn(*args, **kwargs)
		if output is None:
			return

		click.echo(output)
