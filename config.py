import datetime

### Global Configuration
PRICE_URL = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml"
MAX_DATE_CAN_QUERY = 30

### Competition Configuration
COMPETITION_NAME = "sample"
COMPETITION_PATH = "./competition/" + COMPETITION_NAME
COMPETITION_DATA_PATH = COMPETITION_PATH + "/dataset"
COMPETITION_DATA_FILE = COMPETITION_DATA_PATH + "/{}.csv"

### GRAPH
GRAPH_PATH = "graph/{}"
GRAPH_FILE = GRAPH_PATH + "/{}.png"

#VN30 modified
STOCK_LIST = ["CTG", "BID", "BVH", "CTD", "CTG", "EIB", "FPT", "GAS", "HDB", "HPG", "MBB", "MSN", "MWG", "NVL", "PLX", "PNJ", "POW", "REE", "SAB", "SBT", "TCB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]

DATE_FORMAT_STRING = '%d/%m/%Y'
DATASET_TO_DATE = datetime.datetime.today().strftime(DATE_FORMAT_STRING)
DATASET_FROM_DATE = datetime.datetime(2020, 1, 1).strftime(DATE_FORMAT_STRING)

NUM_IGNORED_POINT = 19