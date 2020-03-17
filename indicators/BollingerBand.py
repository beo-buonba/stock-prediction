from .IndicatorCore import IndicatorCore

class BollingerBand(IndicatorCore):
	"""
	Bollinger Band indicator
	"""
	def __init__(self, stock_id, data):
		super(BollingerBand, self).__init__("BollingerBand", stock_id, data)
		self.band = {}
		self.band['base'], self.band['lower'], self.band['upper'] = self.get_bands()

	def get_bands(self):
		"""
		Calculate base, upper, and lower Bollinger Band
		"""
		base = self.sma(20)
		std = self.std_deviation(20)

		upper = []
		lower = []
		for i in range(self.data_length):
			if base[i] == None:
				upper.append(None)
				lower.append(None)
			else:
				upper.append(base[i] + 2 * std[i])
				lower.append(base[i] - 2 * std[i])

		return base, lower, upper


	def graph(self):
		"""
		Plot candle sticks and Bollinger Band		
		"""
		#self.plot_candles(volume_bars=True, overlays=[self.band['upper'], self.band['base'], self.band['lower']])
		self.plot_candles(volume_bars=True, overlays=[self.ema(20)])

		
