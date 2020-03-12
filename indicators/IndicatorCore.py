from abc import abstractmethod
from math import *

class IndicatorCore:
	def __init__(self, name, data):
		self.name = name
		self.data = data
		self.data_length = len(data)

	def sma(self, n):
		sma_sum = 0
		sma = []
		for i in range(self.data_length):
			if (i<n-1):
				sma_sum += self.data[i]['close_price']
				sma.append(None)
			else:
				sma_sum += self.data[i]['close_price']
				sma.append(sma_sum/n)
				sma_sum -= self.data[i-n+1]['close_price']    			
		return sma

	def std_deviation(n):
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


	@abstractmethod
	def indicate(self):
		pass

	@abstractmethod
	def graph(self):
		pass

