import decimal



class Abstract(decimal.Decimal):
	pass



class INR(Abstract):

	class Scale:
		CRORE = 10**7
		LAKH  = 10**5

	def __str__(self):
		if self > self.Scale.CRORE:
			scale = self.Scale.CRORE
			value = (self / scale).quantize(decimal.Decimal('0.01'))
			scale = 'cr'
		
		else:
			scale = self.Scale.LAKH
			value = (self / scale).quantize(decimal.Decimal('0.01'))
			scale = 'lakh'

		return f'₹{value} {scale}'
