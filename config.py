import datetime


### Global Configuration
PRICE_URL = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml"
MAX_DATE_CAN_QUERY = 30

### Competition Configuration
COMPETITION_NAME = "sample"
COMPETITION_PATH = "./competition/" + COMPETITION_NAME
COMPETITION_DATA_PATH = COMPETITION_PATH + "/dataset" 

#VN30 modified
STOCK_LIST = ["CTG", "BID", "BVH", "CTD", "CTG", "EIB", "FPT", "GAS", "HDB", "HPG", "MBB", "MSN", "MWG", "NVL", "PLX", "PNJ", "POW", "REE", "SAB", "SBT", "TCB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]

DATASET_TO_DATE = datetime.datetime.today().strftime('%d/%m/%Y')
DATASET_FROM_DATE = datetime.datetime(2020, 1, 1).strftime('%d/%m/%Y')