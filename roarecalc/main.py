"""
We have found a number of errors in the ROA figures in CBASE05_201502.xlsx. 
This program will recalculate ROA for the company included in this file.
CBASE05_201502.xlsx file is confidential and cannot be released. 
If you have this file, place it in the 'data' directory and run this program.

Github : https://github.com/shion24hub/ROA-recalc
"""

import pandas as pd
import sys

from library.excel.excel import Exproc
from library.db.database import Database
from library.logging.logging import printLog

from config import (
    DB_INIT,
    DEBUG_MODE,
    LOWER_PROCESSING_LIMIT,
    UPPER_PROCESSING_LIMIT,
    EXCEL_COLUMN,
    TEST_EXCEL_PATH,
    PRODUCTION_EXCEL_PATH,
    TEST_DATABASE_PATH,
    PRODUCTION_DATABASE_PATH,
    USING_PERIODS,
    USING_FINANCIAL_FUNCTIONS,
    USING_EXCEL_HEADERS
)

def switcher(debugMode : bool) -> tuple :
    """
    later.
    """
    if debugMode :
        return (TEST_EXCEL_PATH, TEST_DATABASE_PATH)
    else :
        return (PRODUCTION_EXCEL_PATH, PRODUCTION_DATABASE_PATH)

def main() -> None :
    """
    later.
    """
    excelPath, dbPath = switcher(DEBUG_MODE)

    #for excel
    exproc = Exproc(path=excelPath)
    exproc.prepare(headers=USING_EXCEL_HEADERS)

    #for database
    db = Database(path=dbPath)
    if DB_INIT :
        db.init()
    db.connectCursor()

    #main process
    class InvalidDatabaseError(Exception) :
        pass
    def obtainData(tables : list) -> list :
        dataL = []
        lens = []
        for table in tables :
            query = "select {} from info".format(table)
            db.cursor.execute(query)
            data = db.cursor.fetchall()
            dataL.append(data)
            lens.append(len(data))
        
        if len(set(lens)) != 1 :
            error = "Name data, financials data, and balance sheet data are different lengths. Please check the database you are using."
            raise InvalidDatabaseError(error)
        
        return dataL

    dataL = obtainData(["name", "fins", "bs"])
    names = dataL[0]
    fins = dataL[1]
    bss = dataL[2]
    if DEBUG_MODE :
        names = names[LOWER_PROCESSING_LIMIT : UPPER_PROCESSING_LIMIT]
        fins = fins[LOWER_PROCESSING_LIMIT : UPPER_PROCESSING_LIMIT]
        bss = bss[LOWER_PROCESSING_LIMIT : UPPER_PROCESSING_LIMIT]

    processNumber = 0
    normalProcessing = 0
    errorCount = 0
    for name, fin, bs in zip(names, fins, bss) :
        finDf = pd.read_json(fin[0])
        bsDf = pd.read_json(bs[0])
        values = [name[0]]
        errorValues = [name[0]]
        is_error = False
        
        for f in USING_FINANCIAL_FUNCTIONS :
            figures = f(finDf, bsDf, USING_PERIODS)

            #error handling
            if figures == -1 :
                for _ in range(len(USING_EXCEL_HEADERS) - 1) :
                    errorValues.append("ERROR")
                    is_error = True
                break
            
            for figure in figures :
                for value in figure :
                    values.append(value)

        if is_error :
            printLog(USING_EXCEL_HEADERS, errorValues)
            exproc.insert(errorValues)
            errorCount += 1
        else :
            printLog(USING_EXCEL_HEADERS, values)
            exproc.insert(values)
            normalProcessing += 1
        
        processNumber += 1
    
    #excel info
    message1 = "Total Count : {}".format(processNumber)
    message2 = "Normal Processing : {} ({:.3f}%)".format(normalProcessing, normalProcessing / processNumber * 100)
    message3 = "Error Count : {} ({:.3f}%)".format(errorCount, errorCount / processNumber * 100)
    message4 = "Source Code : https://github.com/shion24hub/financial-figure-recalc.git"

    column = EXCEL_COLUMN[len(USING_EXCEL_HEADERS) + 1]
    exproc.write(column + "1", message1)
    exproc.write(column + "2", message2)
    exproc.write(column + "3", message3)
    exproc.write(column + "5", message4)
    
    exproc.finish()
    db.finish()

if __name__ == "__main__" :

    #confirmations
    if DB_INIT and DEBUG_MODE == False :
        print("Database initialization in a production run can have catastrophic results.")
        print("Set debug mode to TRUE and rerun the program.")
        print("Abort the program.")
        sys.exit()

    if DB_INIT :
        confirm = input("Can I really initialize the database? (Y/n)")
        if confirm == "Y" :
            pass
        else :
            print("Interrupts the program (the database is not initialized).")
    
    main()