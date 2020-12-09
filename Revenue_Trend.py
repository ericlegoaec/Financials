
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, rev_gro_calc, rev_trend, ps_scat, group_trend, ps_trend

tickers = ['SMAR', 'AVLR', 'BL', 'COUP', 'TEAM', 'APPF', 'DDOG']
load_fin(userid='', password='', tickers=tickers)

# Import revenue data
fin = import_fin()
stats = import_stats()
revenue = rev_gro_calc(fin)

# Revenue growth trend
group_trend(rev_df=revenue, start_yr=2015)

# Revenue trend
rev_trend(data=revenue, ticker='TEAM')
[rev_trend(revenue, t) for t in tickers]

# Price to Sales Hisotry
ps_trend(data=stats, start_yr=2015)

# Price to Sales Scatter
ps_scat(stats_df=stats, rev_df=revenue)