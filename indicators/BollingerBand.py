

class BollingerBand(IndicatorCore):
	"""
	Calculate and plot Bollinger Band
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


	def graph(self, save_graph=False, show_nontrading=False):
		"""
		Plot candle sticks and Bollinger Band
		:param show_nontrading: show gaps of none trading date or not
		"""

		# Generate ohlc df from data, convert datetime format
		df = pd.DataFrame(self.data)
		ohlc = df.loc[NUM_IGNORED_POINT:, ['date', 'open_price', 'high_price', 'low_price', 'close_price']]
		volumes = list(df["match_volume"][NUM_IGNORED_POINT:])
		fig, ax, formatter, ohlc =  plot_candle_sticks(ohlc, volumes, show_nontrading)

		fig.suptitle('Bollinger Band of {}'.format(self.stock_id))

		# plot bands
		ax.fill_between(ohlc['date'], self.band['lower'][NUM_IGNORED_POINT:], self.band['upper'][NUM_IGNORED_POINT:], facecolor=(1,0,0,.4))
		ax.plot(ohlc['date'], self.band['base'][NUM_IGNORED_POINT:], color='blue')

		ax.xaxis.set_major_formatter(formatter)
		fig.autofmt_xdate()


		if (save_graph):
			if not os.path.exists(GRAPH_PATH.format(self.stock_id)):
				os.makedirs(GRAPH_PATH.format(self.stock_id))
			fig.savefig(GRAPH_FILE.format(self.stock_id, 'Bollinger_Band'))
		else:
			plt.show()
