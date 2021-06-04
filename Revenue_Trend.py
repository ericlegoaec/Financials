
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, fin_calc, rev_trend, ps_scat, \
    group_trend, ps_trend, cost_stats, fcf_sh_trend, fcf_comp_trend, gross_prof, ops_prof, net_prof, \
    kpi_group_trend, kpi_comp_trend, kpi_growth_trend, kpi_vintage_trend

import Ticker_List as tl

tickers = ['AAPL', 'AMD', 'AMZN', 'BAC', 'CSCO', 'FB', 'GE', 'GOOG', 'HPQ', 'IBM', 'INTC', 'MSFT', 'MU', 'NVDA', 'ORCL', 'PFE',
'SPLK', 'NOW', 'WDAY', 'SHOP', 'PYPL', 'OKTA', 'SQ', 'PAYC', 'MDB', 'TWTR', 'NFLX', 'PINS', 'SPOT', 'SNAP', 'ROKU', 'TSLA', 'AMD',
'NXPI', 'SWKS', 'XLNX', 'TXN', 'QRVO', 'AVGO', 'AMAT', 'MRVL', 'DOX', 'SBUX', 'MCD', 'SHAK', 'YUM', 'CELH', 'CMG', 'QCOM', 'XOM', 'CRM',
'AXP', 'MA', 'V', 'FIS', 'ADSK', 'APPF', 'APPS', 'CHKP', 'COUP', 'CTXS', 'CYBR', 'DOCU', 'EVBG', 'FFIV', 'FIVN', 'FTNT',
'HUBS', 'INTU', 'MGNI', 'NEWR', 'PANW', 'PCTY', 'PFPT', 'QLYS', 'RNG', 'TEAM', 'TTD', 'TWLO', 'TYL', 'VEEV', 'VMW', 'ZEN']

load_fin(userid='', password='', tickers=tickers)

# Import revenue data
fin = import_fin()
stats = import_stats()

# Prepare working data frame
revenue = fin_calc(fin, tickers)

# REVENUE TRENDS ############################################################################
# Revenue growth trend
group_trend(rev_df=revenue, tickers=tickers, start_yr=1980)

# Revenue trend on individual comps
rev_trend(data=revenue, ticker='LOW', range=24)
[rev_trend(data=revenue, ticker=t, range=60) for t in tickers]

# PROFIT TRENDS ############################################################################
gross_prof(data=revenue, ticker='TWLO', range=60)
[gross_prof(data=revenue, ticker=t, range=60) for t in tickers]

ops_prof(data=revenue, ticker='TWLO', range=60)
[ops_prof(data=revenue, ticker=t, range=60) for t in tickers]

net_prof(data=revenue, ticker='TWLO', range=36)
[net_prof(data=revenue, ticker=t, range=60) for t in tickers]

# PRICE TO SALES TRENDS #####################################################################
# Price to Sales History
ps_trend(data=stats, tickers=tickers, start_yr=1980)

# Price to Sales Scatter
ps_scat(stats_df=stats, rev_df=revenue, tickers=tickers, type='simple')

# COST ALLOCATION ###########################################################################
# Cost statistics
cost_stats(rev_df=revenue, tickers=tickers)

# FREE CASH FLOWS TRENDS ####################################################################
# Free Cash Flows per share
fcf_sh_trend(data=revenue, tickers=tickers, start_yr=2015)

# Free Cash Flows per share trend on individual comps
fcf_comp_trend(data=revenue, ticker='TWLO', range=60)
[fcf_comp_trend(data=revenue, ticker=t, range=60) for t in tickers]

# KPIs ######################################################################################
# Group based kpi comparison
# ['Gross Merchandise Sales', 'Active Users', 'Active Sellers']
kpi_group_trend(tickers=tickers)

kpi_growth_trend(tickers=tickers, kpi='GMS')

kpi_vintage_trend(tickers=tickers, kpi='GMS')

# Individual kpi trend
kpi_comp_trend(ticker='SHOP', kpi='GMS', range=60)
[kpi_comp_trend(ticker=t, kpi='GMS', range=60) for t in tickers]


