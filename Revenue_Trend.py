
import matplotlib.pyplot as plt

from Financial_Func import load_fin, import_fin, import_stats

load_fin('', '', ['NOW','TWLO', 'DOCU'])

fin = import_fin()
stats = import_stats()

fin[fin.name == 'TotalRevenue'].groupby(['Date', 'Comp'])['Value'].sum().unstack().pct_change()

fin.loc[fin.name == 'TotalRevenue', ['Date', 'Comp', 'Value']].apply(lambda g: )