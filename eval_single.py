import datetime
import os
from DataLoader import DataLoader
from strategies.EMApRSI import EMApRSI
from config import *

if __name__ == "__main__":
	if not os.path.exists(COMPETITION_PATH):
		os.makedirs(COMPETITION_PATH)

	stock_id = STOCK_LIST[0]
	data_loader = DataLoader()
	data = data_loader.collect()[stock_id]



	base_strategy = EMApRSI(COMPETITION_BUDGET, stock_id)
	base_strategy.eval_single(data)