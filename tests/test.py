import yfinance

ticker = yfinance.Ticker("1352.T")
fins = ticker.financials
bs = ticker.balancesheet

netIncome = fins.loc["Net Income"][3]
stock = bs.loc["Total Stockholder Equity"][3]

print(netIncome)
print(stock)

print(netIncome / stock * 100)


