
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, rev_gro_calc, rev_trend, ps_scat, \
    group_trend, ps_trend, cost_stats

import Ticker_List as tl

tickers = tl.SECUR
load_fin(userid='', password='', tickers=tickers)

# Import revenue data
fin = import_fin()
stats = import_stats()
revenue = rev_gro_calc(fin, tickers)

# Revenue growth trend
group_trend(rev_df=revenue, tickers=tickers, start_yr=2016)

# Revenue trend
rev_trend(data=revenue, ticker='DDOG', range=60)
[rev_trend(data=revenue, ticker=t, range=60) for t in tickers]

# Price to Sales History
ps_trend(data=stats, tickers=tickers, start_yr=2017)

# Price to Sales Scatter
ps_scat(stats_df=stats, rev_df=revenue, tickers=tickers)

# Cost statistics
cost_stats(rev_df=revenue, tickers=tickers)

