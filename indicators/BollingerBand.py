from .IndicatorCore import IndicatorCore
import matplotlib.pyplot as plt
from mpl-finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates

class BollingerBand(IndicatorCore):
	def __init__(self, data):
		super(BollingerBand, self).__init__("BollingerBand", data)
		self.data['base'], self.data['lower_band'], self.data['upper_band'] = self.get_bands() 
	
	def get_bands():
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
		df = pd.DataFrame(self.data)

		ohlc = df.loc[:, ['date', 'open_price', 'high_price', 'low_price', 'close_price']]
		ohlc['date'] = pd.to_datetime(ohlc['date'])
		ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
		ohlc = ohlc.astype(float)
		fig, ax = plt.subplots()

		candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

		# Setting labels & titles
		ax.set_xlabel('Date')
		ax.set_ylabel('Price')
		fig.suptitle('Daily Candlestick Chart of NIFTY50')

		# Formatting Date
		date_format = mpl_dates.DateFormatter('%d-%m-%Y')
		ax.xaxis.set_major_formatter(date_format)
		fig.autofmt_xdate()

		fig.tight_layout()

		plt.show()
		

