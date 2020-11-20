
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Financial_Func import load_fin, import_fin, import_stats

load_fin('', '', ['NOW','TWLO', 'DOCU'])

fin = import_fin()
stats = import_stats()


rev_gro = fin[fin.name == 'TotalRevenue'].groupby(['Comp', 'Date'])['Value'].sum().rename('TotalRevenue').reset_index()
rev_gro['Rev_Gro'] = rev_gro.groupby('Comp')['Value'].apply(lambda g: g.pct_change(periods=4))

fin[fin.name == 'CostOfRevenue'].groupby(['Comp', 'Date'])['Value'].sum().reset_index()

# Plot
sns.lineplot(x='Date', y='Rev_Gro', hue='Comp', data=rev_gro)

# Sales to S&M Spend ratio