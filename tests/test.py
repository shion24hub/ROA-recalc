from pprint import pprint
import yfinance

ticker = yfinance.Ticker("1301.T")
pprint(ticker.balancesheet)