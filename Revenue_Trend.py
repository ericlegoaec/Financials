
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats

tickers = ['NOW','TWLO', 'DOCU', 'WDAY', 'OKTA', 'CRWD', 'ZS', 'CRM']
load_fin('', '', tickers)

fin = import_fin()
stats = import_stats()

# Revenue growth analytics
revenue = rev_gro_calc(fin)

# Plot
sns.lineplot(x='Date', y='TotalRevenue_Gro', hue='Comp', data=revenue)

# Sales to S&M Spend ratio