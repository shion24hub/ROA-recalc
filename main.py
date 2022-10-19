"""
We have found a number of errors in the ROA figures in CBASE05_201502.xlsx. 
This program will recalculate ROA for the firms included in this file.
CBASE05_201502.xlsx file is confidential and cannot be released. 
If you have this file, place it in the 'data' directory and run this program.

"""

import pandas as pd
import yfinance
import openpyxl
import string
import logging

import minkabu

DEBUG_MODE = True
ALPHABET = string.ascii_uppercase

#logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)
def printLog(
    dataProcessed : int,
    companyName : str,
    netIncome : float,
    totalAssets : float,
    roa : float
) -> None:
    logging.info("data processed : No.{}".format(dataProcessed))
    logging.info("company name : {}".format(companyName))
    logging.info("net income : {}(yen)".format(netIncome))
    logging.info("total assets : {}(yen)".format(totalAssets))
    logging.info("ROA : {}%".format(roa))


#class for openpyxl processing
class Exproc :
    def __init__(self, path : str) -> None :
        self.path = path
        self.row = 1

    def prepare(self, headers : list, sheet_title = "Sheet") -> None :
        if len(headers) > 26 :
            error = "It only supports 26 letters of the alphabet! Sorry!"
            raise ValueError(error)
        
        self.headers = headers
        self.sheet_title = sheet_title

        wb = openpyxl.Workbook()
        sheet = wb[sheet_title]

        for ind, header in enumerate(headers) :
            cell = ALPHABET[ind] + "1"
            sheet[cell] = header

        self.wb = wb
        self.sheet = sheet
        self.row += 1

    def insert(self, values : list) -> None :
        try :
            self.sheet_title
        except :
            error = "The workbook has not yet been created; use the 'prepare' method."
            raise ValueError(error)

        if len(values) != len(self.headers) :
            error = "The number of values does not match the number of headers."
            raise ValueError(error)
        
        for ind, value in enumerate(values) :
            cell = ALPHABET[ind] + str(self.row)
            self.sheet[cell] = value
        
        self.row += 1
    
    def write(self, cell : str, message : str) :
        self.sheet[cell] = message

    def finish(self) -> None :
        self.wb.save(self.path)

def calcroa(net_income : float, total_assets : float) -> float :
    return net_income / total_assets * 100

def calcroe() :
    pass


if __name__ == "__main__" :

    exproc = Exproc("./data/roacalc.xlsx")
    exproc.prepare(
        headers=["COMPANY NAME", "NET INCOME", "TOTAL ASSETS", "ROA"]
    )
    message = "source code : https://github.com/shion24hub/ROA-recalc"
    exproc.write(
        "F1",
        message,
    )

    #read sheet
    sheet = pd.read_excel("./data/CBASE05_201502.xlsx")
    names = []
    for name in list(sheet["COMNAME"]) :
        names.append(''.join(name.split()))
    
    if DEBUG_MODE :
        names = names[:10]

    nameCodeDict = {}
    for name in names :
        res = minkabu.minkabu(name)

        if len(res) == 0 :
            continue

        ky = list(res.keys())
        va = list(res.values())
        nameCodeDict[ky[0]] = va[0]

    dataProcessed = 1
    for name, scode in nameCodeDict.items() :
        try : 
            scode += ".T"
            ticker = yfinance.Ticker(scode)
            fi = ticker.financials
            bs = ticker.balance_sheet

            netIncome = fi.loc["Net Income"][0]
            totalAssets = bs.loc["Total Assets"][0]
            roa = calcroa(netIncome, totalAssets)
            
            printLog(
                dataProcessed,
                name,
                netIncome,
                totalAssets,
                roa
            )

            exproc.insert(
                values=[name, netIncome, totalAssets, roa]
            )
        except :
            printLog(
                dataProcessed,
                name,
                netIncome,
                totalAssets,
                roa
            )
            exproc.insert(
                values=[name, "ERROR", "ERROR", "ERROR"]
            )

        dataProcessed += 1

exproc.finish()