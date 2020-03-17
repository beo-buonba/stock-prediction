from abc import abstractmethod
from math import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from config import *
from datetime import datetime

class IndicatorCore:
	def __init__(self, name, stock_id, data):
		self.stock_id = stock_id
		self.name = name
		self.data = data
		self.data_length = len(data)

	def sma(self, n):
		sma_sum = 0
		sma = []
		for i in range(self.data_length):
			if (i < n-1):
				sma_sum += self.data[i]['close_price']
				sma.append(None)
			else:
				sma_sum += self.data[i]['close_price']
				sma.append(sma_sum/n)
				sma_sum -= self.data[i-n+1]['close_price']
		return sma

	def ema(self, n):
		ema_sum = 0
		ema = []
		for i in range(self.data_length):
			if (i < n-1):
				ema_sum += self.data[i]['close_price']
				ema.append(None)
			elif (i == n-1 ):
				ema_sum /= n
				ema.append(ema_sum)
			else:
				ema_sum = (self.data[i]['close_price'] - ema_sum) * 2 / (n + 1) + ema_sum
				ema.append(ema_sum)
		return ema

	def std_deviation(self, n):
		sma = self.sma(n)
		std_deviation = []

		for i in range(self.data_length):
			if (i<n-1):
				std_deviation.append(None)
			else:
				square_sum = 0
				for j in range(n):
					tmp = self.data[i-j]['close_price'] - sma[i]
					square_sum += tmp * tmp
				std = sqrt(square_sum/n)
				std_deviation.append(std)

		return std_deviation

	def plot_candles(self, title=None, volume_bars=False, color_function=None,overlays=None, technicals=None, technicals_titles=None):

		def default_color(index, open_price, close_price, low, high):
			return 'r' if open_price[index] > close_price[index] else 'g'

		pricing = pd.DataFrame(self.data)
		pricing = pricing[['open_price',  \
						   'high_price',  \
						   'low_price',   \
						   'close_price', \
						   'match_volume',\
						   'date']]
		pricing['date'] = pricing['date'].apply(lambda date: datetime.strptime(date, DATE_FORMAT_STRING))
		pricing.set_index('date', inplace=True)

		overlays = overlays or []
		color_function = color_function or default_color
		technicals = technicals or []
		technicals_titles = technicals_titles or []
		open_price = pricing['open_price']
		close_price = pricing['close_price']
		low = pricing['low_price']
		high = pricing['high_price']
		oc_min = pd.concat([open_price, close_price], axis=1).min(axis=1)
		oc_max = pd.concat([open_price, close_price], axis=1).max(axis=1)

		if volume_bars:
			fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]})
		else:
			fig, ax1 = plt.subplots(1, 1)
		if title:
			ax1.set_title(title)
		x = np.arange(len(pricing))
		candle_colors = [color_function(i, open_price, close_price, low, high) for i in x]
		candles = ax1.bar(x, oc_max-oc_min, bottom=oc_min, color=candle_colors, linewidth=0)
		lines = ax1.vlines(x - 0.05, low, high, color=candle_colors, linewidth=1)
		ax1.xaxis.grid(False)
		ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off', bottom = 'off')
		time_format = '%m-%y'
	    # Set X axis tick labels.
		date_label = []
		for (c, date) in enumerate(pricing.index):
			if c % 10 == 0:
				date_label.append(date.strftime(time_format))
			else:
				date_label.append("")
		plt.xticks(x, date_label, rotation='vertical')
		for overlay in overlays:
			ax1.plot(x, overlay)
		if volume_bars:
			volume = pricing['match_volume']
			volume_scale = None
			scaled_volume = volume
			if volume.max() > 1000000:
				volume_scale = 'M'
				scaled_volume = volume / 1000000
			elif volume.max() > 1000:
				volume_scale = 'K'
				scaled_volume = volume / 1000
			ax2.bar(x, scaled_volume, color=candle_colors)
			volume_title = 'Volume'
			if volume_scale:
				volume_title = 'Volume (%s)' % volume_scale
			ax2.set_title(volume_title)
			ax2.xaxis.grid(False)
		# Plot additional technical indicators
		for (i, technical) in enumerate(technicals):
			ax = subplots[i - len(technicals)] # Technical indicator plots are shown last
			ax.plot(x, technical)
			if i < len(technicals_titles):
				ax.set_title(technicals_titles[i])
		plt.show()

	@abstractmethod
	def graph(self):
		pass
