import requests
import json
import bs4
import datetime
import os
from  config import *
import csv


class DataCollector:

	def __init__(self):
		self.to_date = DATASET_TO_DATE
		self.from_date = DATASET_FROM_DATE

	@staticmethod
	def get_date(li, class_name, index):
	    """
	    Get date from table and convert format
	    """
	    date = li.find("div",{"class": class_name}).contents[index].strip()
	    date = datetime.datetime.strptime(date, '%Y-%m-%d')
	    return date.strftime('%d/%m/%Y')

	@staticmethod
	def get_change_value(li, class_name, index):
	    """
	    Get value in change column (value & percentage)
	    """
	    value = float(li.find("div",{"class": class_name}).text.split()[index].strip())
	    return value, 1 if value > 0 else -1

	@staticmethod
	def get_trade_value(li, class_name, index):
	    """
	    Get prices and volumn
	    """
	    try:
	        return float(li.findAll("div",{"class": class_name})[index].text.strip())
	    except:
	        return 0

	def get_data_from_id(self, stock_id):		
		from_date = self.from_date
		to_date = self.to_date
		data_table = []

		while True:
			data_form = {
				"searchMarketStatisticsView.symbol": stock_id,
				"strFromDate": from_date,
				"strToDate" : to_date
			}

			r = requests.post(PRICE_URL, data=data_form)
			soup = bs4.BeautifulSoup(r.text, "lxml")
			soup = soup.find("div", {"id": "tab-1"})
			soup = soup.find("ul", {"class": "list_tktt lichsugia"})
			for li in soup:
				try:
					if not li.has_attr('class'):
						data = {}
						data["date"] = self.get_date(li, "row-time noline", 0)
						# From API, only `change_value` has sign ("+/-")
						# So have to add sign manually
						data["change_value"], sign = self.get_change_value(li, "row2", 0)
						data["change_percent"]= sign * self.get_change_value(li, "row2", 1)[0]
						data["open_price"] = self.get_trade_value(li, "row1", 0)
						data["high_price"] = self.get_trade_value(li, "row1", 1)
						data["low_price"] = self.get_trade_value(li, "row1", 2)
						data["close_price"] = self.get_trade_value(li, "row1", 3)
						data["adjust_price"] = self.get_trade_value(li, "row1", 4)
						data["match_volumn"] = self.get_trade_value(li, "row3", 0)
						data["reconcile_volumn"] = self.get_trade_value(li, "row3", 1)

						data_table.append(data)
				except Exception as e:
					# Ignore NavigableString object
					pass
	        # if there is not data on `from_date`
	        # then break when total number of data can be query < max query (30 record/page)
			if data["date"] == from_date or len(soup) < MAX_DATE_CAN_QUERY:
				break
			else:
	        # continue to query
				to_date = data["date"]

		return data_table
	
	def collect_data(self):
		if not os.path.exists(COMPETITION_DATA_PATH):
			os.makedirs(COMPETITION_DATA_PATH)

		for stock_id in STOCK_LIST:
			data = self.get_data_from_id(stock_id)

			filename = COMPETITION_DATA_PATH + "/" + stock_id + ".csv"
			keys = data[0].keys()
			with open(filename, 'w') as output:
				writer = csv.DictWriter(output, keys)
				writer.writeheader()
				writer.writerows(data)


if __name__ == "__main__":
	DC = DataCollector()
	DC.collect_data()