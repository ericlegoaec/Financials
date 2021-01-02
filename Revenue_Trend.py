
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, fin_calc, rev_trend, ps_scat, \
    group_trend, ps_trend, cost_stats, fcf_sh_trend, fcf_comp_trend, gross_prof, ops_prof, net_prof

import Ticker_List as tl

tickers = tl.SECUR
load_fin(userid='', password='', tickers=tickers)

# Import revenue data
fin = import_fin()
stats = import_stats()
revenue = fin_calc(fin, tickers)

# REVENUE TRENDS ############################################################################
# Revenue growth trend
group_trend(rev_df=revenue, tickers=tickers, start_yr=2016)

# Revenue trend on individual comps
rev_trend(data=revenue, ticker='DDOG', range=60)
[rev_trend(data=revenue, ticker=t, range=60) for t in tickers]

# PROFIT TRENDS ############################################################################
gross_prof(data=revenue, ticker='CRWD', range=12)
[gross_prof(data=revenue, ticker=t, range=12) for t in tickers]

ops_prof(data=revenue, ticker='CRWD', range=12)
[ops_prof(data=revenue, ticker=t, range=12) for t in tickers]

net_prof(data=revenue, ticker='CRWD', range=12)
[net_prof(data=revenue, ticker=t, range=12) for t in tickers]

# PRICE TO SALES TRENDS #####################################################################
# Price to Sales History
ps_trend(data=stats, tickers=tickers, start_yr=2017)

# Price to Sales Scatter
ps_scat(stats_df=stats, rev_df=revenue, tickers=tickers)

# COST ALLOCATION ###########################################################################
# Cost statistics
cost_stats(rev_df=revenue, tickers=tickers)

# FREE CASH FLOWS TRENDS ####################################################################
# Free Cash Flows per share
fcf_sh_trend(data=revenue, tickers=tickers, start_yr=2017)

# Free Cash Flows per share trend on individual comps
fcf_comp_trend(data=revenue, ticker='OKTA', range=12)
[fcf_comp_trend(data=revenue, ticker=t, range=60) for t in tickers]

