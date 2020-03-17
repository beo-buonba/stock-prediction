import datetime

### Global Configuration
PRICE_URL = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml"
MAX_DATE_CAN_QUERY = 30

###Constant
DATE_FORMAT_STRING = '%d/%m/%Y'

### Competition Configuration
COMPETITION_NAME = "first"
COMPETITION_PATH = "./competition/" + COMPETITION_NAME
COMPETITION_DATA_PATH = COMPETITION_PATH + "/dataset"
COMPETITION_DATA_FILE = COMPETITION_DATA_PATH + "/{}.csv"
COMPETITION_RESULT_FILE = COMPETITION_PATH + "/{}_result.csv"

DATASET_END_DATE = datetime.datetime.today().strftime(DATE_FORMAT_STRING)
DATASET_START_DATE = datetime.datetime(2019, 1, 1).strftime(DATE_FORMAT_STRING)

EVAL_END_DATE = datetime.datetime.today().strftime(DATE_FORMAT_STRING)
EVAL_START_DATE = datetime.datetime(2019, 7, 1).strftime(DATE_FORMAT_STRING)

COMPETITION_BUDGET = 5000
#VN30 modified
#STOCK_LIST = ["CTG", "BID", "BVH", "CTD", "CTG", "EIB", "FPT", "GAS", "HDB", "HPG", "MBB", "MSN", "MWG", "NVL", "PLX", "PNJ", "POW", "REE", "SAB", "SBT", "TCB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]

#Test
STOCK_LIST = ["CTG"]



