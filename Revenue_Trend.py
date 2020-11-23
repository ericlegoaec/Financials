
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats, rev_gro_calc, rev_trend

tickers = ['TWLO', 'DOCU', 'OKTA', 'CRWD', 'ZS']
load_fin('', '', tickers)

fin = import_fin()
stats = import_stats()

# Revenue growth analytics
revenue = rev_gro_calc(fin)

# Plot
sns.lineplot(x='Date', y='TotalRevenue_Gro', hue='Comp', data=revenue)

sns.barplot(x='Date', y='TotalRevenue', hue='Comp', data=revenue[revenue.Comp == 'TWLO'])


rev_trend(data=revenue, ticker='OKTA')