import pandas as pd

def calcroa(fins : pd.DataFrame, bs : pd.DataFrame) -> tuple :

    """
    later.
    """

    roaL = []
    netIncomeL = []
    totalAssetL = []
    for period in range(4) :
        netIncome = fins.loc["Net Income"][period]
        totalAssets = bs.loc["Total Assets"][period]
        roa = netIncome / totalAssets * 100

        roaL.append(roa)
        netIncomeL.append(netIncome)
        totalAssetL.append(totalAssets)
    
    return (roaL, netIncomeL, totalAssetL)

def calcroe() :

    """
    later.
    """

    pass