import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ohlc
from .IndicatorCore import IndicatorCore
from utils.graph_utils import IntegerIndexDateTimeFormatter
from config import DATE_FORMAT_STRING, NUM_IGNORED_POINT


class BollingerBand(IndicatorCore):
	"""
	Calculate and plot Bollinger Band
	"""
	def __init__(self, data):
		super(BollingerBand, self).__init__("BollingerBand", data)

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


	def graph(self, show_nontrading=False):
		"""
		Plot candle sticks and Bollinger Band
		:param show_nontrading: show gaps of none trading date or not
		"""

		# Generate ohlc df from data, convert datetime format
		df = pd.DataFrame(self.data)
		ohlc = df.loc[NUM_IGNORED_POINT:, ['date', 'open_price', 'high_price', 'low_price', 'close_price']]
		ohlc['date'] = pd.to_datetime(ohlc['date'], format=DATE_FORMAT_STRING)
		ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
		ohlc = ohlc.astype(float)

		# Formatting Date for plotting
		if show_nontrading:
			formatter = mpl_dates.DateFormatter(DATE_FORMAT_STRING)
		else:
			formatter = IntegerIndexDateTimeFormatter(list(ohlc['date']), DATE_FORMAT_STRING)
			ohlc['date'] = np.arange(len(ohlc['date']))

		# Define subplots, setting labels & titles
		fig, ax = plt.subplots()
		ax.set_xlabel('Date')
		ax.set_ylabel('Price')
		fig.suptitle('Bollinger Band')

		# plot candle sticks to subplot
		candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

		# plot bands
		ax.fill_between(ohlc['date'], self.band['lower'][NUM_IGNORED_POINT:], self.band['upper'][NUM_IGNORED_POINT:], facecolor=(1,0,0,.4))
		ax.plot(ohlc['date'], self.band['base'][NUM_IGNORED_POINT:], color='blue')

		ax.xaxis.set_major_formatter(formatter)
		fig.autofmt_xdate()
		fig.tight_layout()
		plt.show()
