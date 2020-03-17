from abc import abstractmethod
from config import *
from datetime import datetime

class StrategyCore():
	def __init__(self, name, budget, stock_id, start_date):
		self.name = name		
		self.budget = budget
		self.stock_id = stock_id
		self.start_date = start_date

		self.asset = budget
		self.portfolio = []
		self.orders_book = []

	@abstractmethod
	def order(self, data_line):
		pass

	def eval_single(self, data, end_date=EVAL_END_DATE, print_result=True):
		end_date = datetime.strptime(end_date, DATE_FORMAT_STRING)
		start_date = datetime.strptime(self.start_date, DATE_FORMAT_STRING)
		for data_line in reversed(data):
			date  = datetime.strptime(data_line["date"], DATE_FORMAT_STRING)
			if date > end_date:
				break
			if date >= start_date:
				self.order(data_line)
		if print_result:
			print("---------RESULT:---------")
			print()
			print("Strategy name: %s" %self.name)
			print("Stock: %s" %self.stock_id)
			print("Budget: %.2f" %self.budget)
			duration = end_date - start_date
			print("Duration: %d days (%s -> %s)" %(duration.days, start_date, end_date))
			print("Profit/Loss: %.2f%%" %((self.asset/self.budget - 1)*100))
			print()
			print("-------------------------")
