from .StrategyCore import StrategyCore
from config import *

class EMApRSI(StrategyCore):
	def __init__(self, budget, stock_id, start_date=EVAL_START_DATE):
		super(EMApRSI, self).__init__("EMApRSI", budget, stock_id, start_date)
