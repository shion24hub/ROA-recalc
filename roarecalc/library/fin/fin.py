import pandas as pd

def calcroa(fins : pd.DataFrame, bs : pd.DataFrame, periods = 4) -> tuple :

    """
    later.
    """

    netIncomeL = []
    totalAssetL = []
    roaL = []
    for period in range(periods) :
        try :
            netIncome = fins.loc["Net Income"][period]
            totalAssets = bs.loc["Total Assets"][period]
            roa = netIncome / totalAssets * 100

            roaL.append(roa)
            netIncomeL.append(netIncome)
            totalAssetL.append(totalAssets)
        except :
            return -1
    
    return (netIncomeL, totalAssetL, roaL)

def calcroe(fins : pd.DataFrame, bs : pd.DataFrame, periods = 4) -> tuple :

    """
    later.
    """

    netIncomeL = []
    netWorthL = []
    roeL = []
    for period in range(periods) :
        try :
            netIncome = fins.loc["Net Income"][period]
            netWorth = bs.loc["Total Stockholder Equity"][period]
            roe = netIncome / netWorth * 100

            roeL.append(roe)
            netIncomeL.append(netIncome)
            netWorthL.append(netWorth)
        except :
            return -1
    
    return (netIncomeL, netWorthL, roeL)