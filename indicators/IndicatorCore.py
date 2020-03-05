

class IndicatorCore:
	def __init__(self, name, data):
        self.name = name
        self.data = data
        self.data_length = len(data)

    def sma(self, n):
    	sma_sum = 0
    	sma = []
    	for i in range(self.data_length):
    		if (i<n):
    			sma_sum += self.data[i]['close_price']
    			sma.append(None)
    		else:
    			sma.append(sma_sum/n)
    			sma_sum -= self.data[i-n]['close_price']
    			sma_sum += self.data[i]['close_price']
    	return sma



    @abstractmethod
    def indicate(self):
        pass

    @abstractmethod
    def graph(self):
    	pass

