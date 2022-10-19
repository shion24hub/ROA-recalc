"""
We have found a number of errors in the ROA figures in CBASE05_201502.xlsx. 
This program will recalculate ROA for the for the company included in this file.
CBASE05_201502.xlsx file is confidential and cannot be released. 
If you have this file, place it in the 'data' directory and run this program.

Github : https://github.com/shion24hub/ROA-recalc
"""

import pandas as pd
import yfinance
import openpyxl
import os
import string
import logging
import sqlite3
import time

import minkabu

DEBUG_MODE = True
ALPHABET = string.ascii_uppercase
UPPER_PROCESSING_LIMIT = 1000

#logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)
def printLog(
    dataProcessed : int,
    companyName : str,
    netIncome_0 : float,
    totalAssets_0 : float,
    netIncome_1 : float,
    totalAssets_1 : float,
    netIncome_2 : float,
    totalAssets_2 : float,
    netIncome_3 : float,
    totalAssets_3 : float,
    roa_0 : float,
    roa_1 : float,
    roa_2 : float,
    roa_3 : float,
) -> None:
    logging.info("\ndata processed : No.{}".format(dataProcessed))
    logging.info("company name : {}".format(companyName))
    logging.info("net income-0 : {} (yen)".format(netIncome_0))
    logging.info("total assets-0 : {} (yen)".format(totalAssets_0))
    logging.info("net income-1 : {} (yen)".format(netIncome_1))
    logging.info("total assets-1 : {} (yen)".format(totalAssets_1))
    logging.info("net income-2 : {} (yen)".format(netIncome_2))
    logging.info("total assets-2 : {} (yen)".format(totalAssets_2))
    logging.info("net income-3 : {} (yen)".format(netIncome_3))
    logging.info("total assets-3 : {} (yen)".format(totalAssets_3))
    logging.info("ROA-0 : {} (%)".format(roa_0))
    logging.info("ROA-1 : {} (%)".format(roa_1))
    logging.info("ROA-2 : {} (%)".format(roa_2))
    logging.info("ROA-3 : {} (%)\n".format(roa_3))

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

#for Database class
class YetClosedError(Exception) :
    pass

class Database :
    def __init__(self, path : str) :
        self.path = path
        self.nowConnect = False
    
    def connectCursor(self) :
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        self.nowConnect = True
        self.connection = connection
        self.cursor = cursor
    
    def init(self) :
        if self.nowConnect :
            error = "Connection to the database is not closed, use the finish method."
            raise YetClosedError(error)

        is_file = os.path.isfile(self.path)
        if is_file :
            os.remove(self.path)
        
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        sql = "create table info(name string, fins json, bs json)"
        cursor.execute(sql)

        connection.commit()
        connection.close()

    def finish(self) :
        self.nowConnect = False
        self.connection.commit()
        self.connection.close()

def calcroa(net_income : float, total_assets : float) -> float :
    return net_income / total_assets * 100

def calcroe() :
    pass

if __name__ == "__main__" :

    #for excel
    exproc = Exproc("./data/roacalc.xlsx")
    exproc.prepare(
        headers=[
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
    )

    #for database
    db = Database("./db/companyInfo.db")

    if DEBUG_MODE :
        db.init()
    
    db.connectCursor()

    #read sheet
    sheet = pd.read_excel("./data/CBASE05_201502.xlsx")
    names = []
    for name in list(sheet["COMNAME"]) :
        names.append(''.join(name.split()))
    
    if DEBUG_MODE :
        names = names[:5]
    else :
        names = names[:UPPER_PROCESSING_LIMIT]

    nameCodeDict = {}
    for ind, name in enumerate(names) :
        res = minkabu.minkabu(name)

        if len(res) == 0 :
            continue

        ky = list(res.keys())
        va = list(res.values())
        nameCodeDict[ky[0]] = va[0]

        if ind % 50 == 0 :
            print("\nThe system goes into a 10-second sleep.\n")
            time.sleep(10)
            print("\nSleep for 10 seconds has been completed. Processing will continue.\n")

    dataProcessed = 1
    countError = 0
    normalProcessing = 0
    for name, scode in nameCodeDict.items() :
        try : 
            scode += ".T"
            ticker = yfinance.Ticker(scode)
            fi = ticker.financials
            bs = ticker.balance_sheet

            #save to db
            fiJson = fi.to_json()
            bsJson = bs.to_json()
            insertQuery = "insert into info values(?, ?, ?)"

            insertInfo = [(name, fiJson, bsJson)]
            db.cursor.executemany(insertQuery, insertInfo)

            netIncome_0 = fi.loc["Net Income"][0]
            netIncome_1 = fi.loc["Net Income"][1]
            netIncome_2 = fi.loc["Net Income"][2]
            netIncome_3 = fi.loc["Net Income"][3]
            totalAssets_0 = bs.loc["Total Assets"][0]
            totalAssets_1 = bs.loc["Total Assets"][1]
            totalAssets_2 = bs.loc["Total Assets"][2]
            totalAssets_3 = bs.loc["Total Assets"][3]
            roa_0 = calcroa(netIncome_0, totalAssets_0)
            roa_1 = calcroa(netIncome_1, totalAssets_1)
            roa_2 = calcroa(netIncome_2, totalAssets_2)
            roa_3 = calcroa(netIncome_3, totalAssets_3)
            
            printLog(
                dataProcessed,
                name,
                netIncome_0,
                totalAssets_0,
                netIncome_1,
                totalAssets_1,
                netIncome_2,
                totalAssets_2,
                netIncome_3,
                totalAssets_3,
                roa_0,
                roa_1,
                roa_2,
                roa_3
            )

            exproc.insert(
                values=[
                    name, 
                    netIncome_0,
                    totalAssets_0,
                    netIncome_1,
                    totalAssets_1,
                    netIncome_2,
                    totalAssets_2,
                    netIncome_3,
                    totalAssets_3, 
                    roa_0,
                    roa_1,
                    roa_2,
                    roa_3
                ]
            )
            normalProcessing += 1
        except :
            countError += 1
            printLog(
                dataProcessed,
                name,
                netIncome_0,
                totalAssets_0,
                netIncome_1,
                totalAssets_1,
                netIncome_2,
                totalAssets_2,
                netIncome_3,
                totalAssets_3,
                roa_0,
                roa_1,
                roa_2,
                roa_3
            )

            values=[name]
            for _ in range(12) :
                values.append("ERROR")
            exproc.insert(
                values
            )

        dataProcessed += 1
    
    """
    TODO :The following process will result in an error. The reason is under investigation.
    """
    # try :
    #     message1 = "Total count : " + str(dataProcessed)
    #     message2 = "Normal processing : " + str(normalProcessing)
    #     message3 = "error count : " + str(countError)
    #     message4 = "source code : https://github.com/shion24hub/ROA-recalc"
    #     messages = [message1, message2, message3, message4]
    #     for i in range(4) :
    #         cell = "O" + str(i)
    #         exproc.write(
    #             cell,
    #             messages[i]
    #         )
    # except :
    #     pass
    message1 = "Total count : " + str(dataProcessed - 1)
    message2 = "Normal processing : " + str(normalProcessing)
    message3 = "error count : " + str(countError)
    message4 = "source code : https://github.com/shion24hub/ROA-recalc"

    exproc.write("O1", message1)
    exproc.write("O2", message2)
    exproc.write("O3", message3)
    exproc.write("O4", message4)

    
    db.finish()
    exproc.finish()