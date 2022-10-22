from library.fin.fin import (
    calcroa,
    calcroe,
)

#config
READ_FROM_SHEET : bool = False
DB_INIT : bool = False
DEBUG_MODE : bool = False
LOWER_PROCESSING_LIMIT : int = 0
UPPER_PROCESSING_LIMIT : int = 1000
TEST_EXCEL_PATH : str = "./product/test.xlsx"
PRODUCTION_EXCEL_PATH : str = "./product/product.xlsx"
TEST_DATABASE_PATH : str = "./db/test.db"
PRODUCTION_DATABASE_PATH : str = "./db/companyInfo.db"
USING_FINANCIAL_FUNCTIONS : list = [
    calcroa,
    calcroe,
]
USING_EXCEL_HEADERS : list = [
    "COMPANY NAME",
    "NET INCOME-0 (yen)",
    "TOTAL ASSETS-0 (yen)",
    "NET INCOME-1 (yen)",
    "TOTAL ASSETS-1 (yen)",
    "NET INCOME-2 (yen)",
    "TOTAL ASSETS-2 (yen)",
    "NET INCOME-3 (yen)",
    "TOTAL ASSETS-3 (yen)",
    "ROA-0 (%)",
    "ROA-1 (%)",
    "ROA-2 (%)",
    "ROA-3 (%)"
]