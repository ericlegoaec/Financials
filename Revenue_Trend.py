
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, rev_gro_calc, rev_trend

tickers = ['FSLY', 'NET', 'CRWD', 'ZS', 'OKTA', 'TWLO', 'DOCU', 'TTD', 'DDOG', 'ESTC']
load_fin('', '', tickers)

fin = import_fin()
stats = import_stats()

# Revenue data frame
revenue = rev_gro_calc(fin)

# Revenue growth trend
sns.lineplot(x='Date', y='TotalRevenue_Gro', hue='Comp', data=revenue).set_title('Revenue Growth Trend')

# Revenue trend
rev_trend(data=revenue, ticker='CRWD')

# Price to Sales Hisotry
sns.lineplot(x='Date', y='Value', hue='Comp', data=stats.loc[(stats.name == 'PsRatio'), :]).set_title('P/S Ratio Trend')

# Price to Sales Scatter
ps_scat(stats_df=stats, rev_df=revenue)