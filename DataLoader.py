import requests
import bs4
import os
import csv
from  config import *


class DataLoader:
    """
    Crawl data from vndirect
    """
    def __init__(self, to_date=DATASET_TO_DATE, from_date=DATASET_FROM_DATE, stock_list=STOCK_LIST):
        self.to_date = to_date
        self.from_date = from_date
        self.stock_list = stock_list

    @staticmethod
    def get_date(li, class_name, index):
        """
        Get date from table and convert format
        """
        date = li.find("div",{"class": class_name}).contents[index].strip()
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return date.strftime(DATE_FORMAT_STRING)

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

    @staticmethod
    def get_data_from_id(start_date, end_date, stock_id):
        """
        Query data with stock_id, start_date, end_date
        :return: list of data dict
        """
        from_date = start_date
        to_date = end_date
        data_table = []
        date_set = set() # Prevend duplicates

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
                        data["date"] = DataLoader.get_date(li, "row-time noline", 0)
                        if data["date"] in date_set:
                            continue
                        date_set.add(data["date"])
                        # From API, only `change_value` has sign ("+/-")
                        # So have to add sign manually
                        data["change_value"], sign = DataLoader.get_change_value(li, "row2", 0)
                        data["change_percent"]= sign * DataLoader.get_change_value(li, "row2", 1)[0]
                        data["open_price"] = DataLoader.get_trade_value(li, "row1", 0)
                        data["high_price"] = DataLoader.get_trade_value(li, "row1", 1)
                        data["low_price"] = DataLoader.get_trade_value(li, "row1", 2)
                        data["close_price"] = DataLoader.get_trade_value(li, "row1", 3)
                        data["adjust_price"] = DataLoader.get_trade_value(li, "row1", 5)
                        data["match_volume"] = DataLoader.get_trade_value(li, "row3", 0)
                        data["reconcile_volume"] = DataLoader.get_trade_value(li, "row3", 1)
                        if data["close_price"] != data["adjust_price"]:
                            data['open_price'] = data["adjust_price"] * data["open_price"] / data["close_price"]
                            data['high_price'] = data["adjust_price"] * data["high_price"] / data["close_price"]
                            data['low_price'] = data["adjust_price"] * data["low_price"] / data["close_price"]
                            data['close_price'] = data["adjust_price"]
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

    def collect(self):
        """
        Collect data and stored
        """
        if not os.path.exists(COMPETITION_DATA_PATH):
            os.makedirs(COMPETITION_DATA_PATH)

        for stock_id in self.stock_list:
            data = DataLoader.get_data_from_id(self.from_date, self.to_date, stock_id)

            filename = COMPETITION_DATA_FILE.format(stock_id)
            keys = data[0].keys()
            with open(filename, 'w') as output:
                writer = csv.DictWriter(output, keys)
                writer.writeheader()
                writer.writerows(data)

    def load(self):
        """
        Get data from vndirect
        :return:
        """
        self.data = self.get_data_from_id(self.from_date, self.to_date, self.stock_list)
        self.data = self.data[::-1] # reverse date (ascending)
        return self.data


if __name__ == "__main__":
    data_loader = DataLoader()
    data_loader.collect()
