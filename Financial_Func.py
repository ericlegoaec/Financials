"""
FUNCTIONS

@author:    Gerard Mazi
@date:      2020-10-30
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

from selenium import webdriver
import time
import os
import glob
import pandas as pd
from datetime import date

###############################################################################################
# Download financials
def load_fin(userid, password, tickers):

    # Clear prior downloads
    downloads = glob.glob('C:/Users/gerard/Downloads/*')
    for d in downloads:
        os.remove(d)

    # Open Chrome
    driver = webdriver.Chrome(r"chromedriver.exe")
    driver.maximize_window()
    driver.get('https://login.yahoo.com/')
    time.sleep(2)

    # Login - Username
    driver.find_element_by_xpath('//*[@class="phone-no "]').send_keys(userid)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login-signin"]').click()
    time.sleep(2)

    # Login - Password
    driver.find_element_by_xpath('//*[@class="password"]').send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login-signin"]').click()
    time.sleep(5)

    for t in tickers:

        statements = ['/financials?p=', '/balance-sheet?p=', '/cash-flow?p=', '/key-statistics?p=']

        for s in statements:

            driver.get('https://finance.yahoo.com/quote/' + t + s + t)
            time.sleep(3)
            driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
            time.sleep(3)

    driver.quit()

    del downloads, d, driver, statements

###############################################################################################
# Merge financials

def import_fin():
    files = [f for f in glob.glob('C:/Users/gerard/Downloads/*') if 'valuation' not in f]
    financials = pd.DataFrame({'Comp': [], 'name': [], 'Date': [], 'Value': []})

    for f in range(len(files)):
        file = pd.read_csv(files[f], thousands=',')
        file['Comp'] = files[f][26:30].replace('_', '')
        file = pd.melt(file, id_vars=['Comp', 'name'], var_name='Date', value_name='Value')

        financials = pd.concat([financials, file], axis=0, ignore_index=True)
        financials = financials.loc[financials.Date != 'ttm', :]

        # Format
        financials['Date'] = pd.to_datetime(financials['Date'])
        financials['Value'] = pd.to_numeric(financials['Value'])

    return financials

    del file, f, files

###############################################################################################
# Merge stats

def import_stats():
    files = [f for f in glob.glob('C:/Users/gerard/Downloads/*') if 'valuation' in f]
    stats = pd.DataFrame({'Comp': [], 'name': [], 'Date': [], 'Value': []})

    for f in range(len(files)):
        file = pd.read_csv(files[f], thousands=',')
        file['Comp'] = files[f][26:30].replace('_', '')
        file = pd.melt(file, id_vars=['Comp', 'name'], var_name='Date', value_name='Value')

        stats = pd.concat([stats, file], axis=0, ignore_index=True)
        stats.loc[stats.Date == 'ttm', 'Date'] = date.today()

        # Format
        stats['Date'] = pd.to_datetime(stats['Date'])

    return stats

    del file, f, files

################################################################################################
# Revenue Growth Trend

def growth_calc(data):
    field = [
        'TotalRevenue', 'CostOfRevenue', 'OtherGandA', 'SellingAndMarketingExpense' ,
        'ResearchAndDevelopment', 'OperatingIncome'
    ]

    # Calc year over year growth rate
    for f in field[: -1]:
        rev_temp = fin.groupby(['Comp', 'Date'])
        rev_temp[f] = pd.Series(fin[fin.name == f].groupby(['Comp', 'Date'])['Value'].sum().rename(f), index=rev_temp)
        rev_temp[f + '_gro'] = pd.Series(rev_temp.groupby('Comp')[f].apply(lambda g: g.pct_change(periods=4)))

    del f

    # Calc cost as a percent of revenue
    for f in  field[: -1][1:]:
        rev_temp[rev_temp.f]