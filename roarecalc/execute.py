def readFromDB() -> None :
    pass

    sheet = pd.read_excel("./data/CBASE05_201502.xlsx")
    names = []
    for name in list(sheet["COMNAME"]) :
        names.append(''.join(name.split()))
    
    if DEBUG_MODE :
        names = names[:5]
    else :
        names = names[LOWER_PROCESSING_LIMIT:UPPER_PROCESSING_LIMIT]

    nameCodeDict = {}
    noData = []
    for ind, name in enumerate(names) :
        res = minkabu(name)

        if len(res) == 0 :
            noData.append(name)
            nameCodeDict[name] = "0000"
            continue

        ky = list(res.keys())
        va = list(res.values())
        nameCodeDict[ky[0]] = va[0]

        if ind == 0 :
            continue
        if ind % 50 == 0 :
            print("\nThe system goes into a 10-second sleep.\n")
            time.sleep(10)
            print("\nSleep for 10 seconds has been completed. Processing will continue.\n")

    #Obtaining Financial Statements and Calculating ROA
    dataProcessed = 1
    countError = 0
    countNoData = 0
    normalProcessing = 0
    for name, scode in nameCodeDict.items() :
        try : 
            if scode == "0000" :
                values = [name]
                for _ in range(12) :
                    values.append("NO-DATA")
                exproc.insert(
                    values
                )
                countNoData += 1
                #TODO : デザイン的にtryexceptの下に統一すべき
                dataProcessed += 1
                continue

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
    try :
        message1 = "Total count : {}".format(dataProcessed - 1)
        message2 = "Normal processing : {} ({:.3f}%)".format(normalProcessing, normalProcessing / dataProcessed * 100)
        message3 = "error count : {} ({:.3f}%)".format(countError, countError / dataProcessed * 100)
        message4 = "no-data count : {} ({:.3f}%)".format(countNoData, countNoData / dataProcessed * 100)

        message5 = "error : Delisting and other reasons (program bug etc.)" 
        message6 = "no-data : The company name has changed, or the company was never listed in the first place and other reasons (program bug etc.)"

        message7 = "source code : https://github.com/shion24hub/ROA-recalc"

        exproc.write("O1", message1)
        exproc.write("O2", message2)
        exproc.write("O3", message3)
        exproc.write("O4", message4)

        exproc.write("O6", message5)
        exproc.write("O7", message6)

        exproc.write("O9", message7)
    except :
        pass

    print("no data : {}".format(noData))
    db.finish()
    exproc.finish()