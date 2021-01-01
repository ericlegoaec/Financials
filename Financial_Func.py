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
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

###############################################################################################
# Download financials
def load_fin(userid, password, tickers):

    # Clear prior downloads
    downloads = glob.glob('C:/Users/gmazi/Downloads/*')
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

        # Income Statement
        driver.get('https://finance.yahoo.com/quote/' + t + '/financials?p=' + t)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]'
        ).click()
        time.sleep(3)

        # Balance Sheet
        driver.get('https://finance.yahoo.com/quote/' + t + '/balance-sheet?p=' + t)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]'
        ).click()
        time.sleep(3)

        # Cash Flows
        driver.get('https://finance.yahoo.com/quote/' + t + '/cash-flow?p=' + t)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]'
        ).click()
        time.sleep(3)

        # Statistics
        driver.get('https://finance.yahoo.com/quote/' + t + '/key-statistics?p=' + t)
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]'
        ).click()
        time.sleep(3)

    driver.quit()

    del downloads, d, driver, t

###############################################################################################
# Merge financials

def import_fin():
    files = [f for f in glob.glob('C:/Users/gmazi/Downloads/*') if 'valuation' not in f]
    financials = pd.DataFrame({'Comp': [], 'name': [], 'Date': [], 'Value': []})

    for f in range(len(files)):

        # Load file
        file = pd.read_csv(files[f], thousands=',')

        # Cleanup ticker
        file['Comp'] = files[f][25:30].replace('_', '').replace('q', '').replace('u', '')

        # Convert to long format
        file = pd.melt(file, id_vars=['Comp', 'name'], var_name='Date', value_name='Value')

        # Append
        financials = pd.concat([financials, file], axis=0, ignore_index=True)
        financials = financials.loc[financials.Date != 'ttm', :]

        # Format
        financials['Date'] = pd.to_datetime(financials['Date'])
        financials['Value'] = pd.to_numeric(financials['Value'])
        financials['name'] = financials.name.str.strip()

    return financials

    del file, f, files

###############################################################################################
# Merge stats

def import_stats():
    files = [f for f in glob.glob('C:/Users/gmazi/Downloads/*') if 'valuation' in f]
    stats = pd.DataFrame({'Comp': [], 'name': [], 'Date': [], 'Value': []})

    for f in range(len(files)):

        # Load file
        file = pd.read_csv(files[f], thousands=',', skipinitialspace=True)

        # Cleanup ticker
        file['Comp'] = files[f][25:30].replace('_', '').replace('q', '').replace('u', '')

        # Convert to long format
        file = pd.melt(file, id_vars=['Comp', 'name'], var_name='Date', value_name='Value')

        # Append
        stats = pd.concat([stats, file], axis=0, ignore_index=True)
        stats.loc[stats.Date == 'ttm', 'Date'] = date.today()

        # Format
        stats['Date'] = pd.to_datetime(stats['Date'])
        stats['name'] = stats.name.str.strip()

    return stats

    del file, f, files

################################################################################################
# Revenue Growth Data Frame

def rev_gro_calc(data, tickers):
    field = [
        'TotalRevenue', 'CostOfRevenue', 'OtherGandA', 'SellingAndMarketingExpense',
        'ResearchAndDevelopment', 'OperatingIncome'
    ]

    # Calc year over year growth rate
    data = data[data.Comp.isin(tickers)]
    rev = data.groupby(['Comp', 'Date'])['Value'].sum().reset_index()[['Comp', 'Date']]

    # Calc revenue growth
    for f in field[: -1]:
        rev_temp = data[data.name == f].groupby(['Comp', 'Date'])['Value'].sum().rename(f).reset_index()
        rev_temp[f + '_Gro'] = rev_temp.groupby('Comp')[f].apply(lambda g: g.pct_change(periods=4))

        rev = pd.merge(rev, rev_temp, how='left', on=['Comp', 'Date'])

    # Calc cost pct of revenue
    rev['S&M_pct_Rev'] = rev.SellingAndMarketingExpense / rev.TotalRevenue
    rev['R&D_pct_Rev'] = rev.ResearchAndDevelopment / rev.TotalRevenue

    # Calc revenue per cost
    rev['Rev_per_S&M'] = rev.TotalRevenue / rev.SellingAndMarketingExpense
    rev['Rev_per_R&D'] = rev.TotalRevenue / rev.ResearchAndDevelopment

    return rev

    del f, field, rev_temp, rev


################################################################################################
# Group Revenue Growth Trends
def group_trend(rev_df, tickers, start_yr=2010):

    rev_df = rev_df[rev_df.Comp.isin(tickers)]

    plt.figure()
    sns.lineplot(
        x='Date',
        y='TotalRevenue_Gro',
        hue='Comp',
        data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3
    ).set_title('Revenue Growth Trend')
    plt.grid()
    plt.show()

    print(rev_df.groupby(['Date', 'Comp'])['TotalRevenue_Gro'].sum().unstack()[str(start_yr):])

################################################################################################
# Individual Stock Revenue Trends

def rev_trend(data, ticker, range=60):

    # Source Data
    rev_stats = data.loc[
        data.Comp == ticker,
        [
            'Date',
            'TotalRevenue',
            'TotalRevenue_Gro',
            'CostOfRevenue_Gro',
            'OtherGandA_Gro',
            'SellingAndMarketingExpense_Gro',
            'ResearchAndDevelopment_Gro'
        ]
    ]

    # Format to Millions
    rev_stats['TotalRevenue'] = rev_stats.TotalRevenue / 1000000

    # Time frame
    rev_stats = rev_stats.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(rev_stats.Date, rev_stats.TotalRevenue, width=80, color='Lightgray', label='Revenue')
    ax2.plot(rev_stats.Date, rev_stats['TotalRevenue_Gro'], 'o-', color='black', label='Revenue Growth', linewidth=3)
    #ax2.plot(rev_stats.Date, rev_stats['CostOfRevenue_Gro'], '.-', color='purple', label='COGS Growth')
    #ax2.plot(rev_stats.Date, rev_stats['OtherGandA_Gro'], '.-', color='orange', label='G&A Growth')
    ax2.plot(rev_stats.Date, rev_stats['SellingAndMarketingExpense_Gro'], '.-', color='green', label='S&M Growth')
    ax2.plot(rev_stats.Date, rev_stats['ResearchAndDevelopment_Gro'], '.-', color='blue', label='R&D Growth')

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Total Revenue (millions)')
    ax2.set_ylabel('Growth Rate (YoY)')
    plt.title(ticker +  ' Revenue Growth (YoY)')
    plt.grid(True)
    plt.show()



################################################################################################
# Price/Sales Group Trend
def ps_trend(data, tickers, start_yr=2010):

    data = data[data.Comp.isin(tickers)]
    data = data.loc[(data.name == 'PsRatio') & (data.Date >= str(start_yr)), :]

    plt.figure()
    sns.lineplot(
        x='Date',
        y='Value',
        hue='Comp',
        data=data,
        linewidth=3
    )
    plt.ylabel('Price/Sales Ratio')
    plt.title('P/S Ratio Trend')
    plt.grid()
    plt.show()

    print(data.groupby(['Date', 'Comp'])['Value'].sum().unstack())


################################################################################################
# Price/Sales Group Scatter Plot

def ps_scat(stats_df, rev_df, tickers):
    stats_df = stats_df[stats_df.Comp.isin(tickers)]
    scat = pd.merge(
        stats_df.loc[stats_df.Date == stats_df.Date.max()]
            .groupby(['Comp', 'name'])['Value']
            .sum()
            .unstack()[['PsRatio']],
        pd.merge(
            rev_df.groupby(['Comp'])['Date'].max(),
            rev_df[['Comp', 'Date', 'TotalRevenue_Gro', 'TotalRevenue']],
            how='left',
            on=['Comp', 'Date']
        )[['Comp', 'TotalRevenue_Gro', 'TotalRevenue']],
        how='left',
        on='Comp'
    )

    radius = scat.TotalRevenue/1000000

    plt.figure()
    ax = plt.subplot(111)
    plt.grid(True)
    ax.plot([0, 1], [0, 1], color='red', transform=ax.transAxes, linewidth=0.5)
    ax.scatter(x=scat.PsRatio, y=scat.TotalRevenue_Gro, alpha=0.5, s=radius)
    ax.set_ylabel('Revenue Growth')
    ax.set_xlabel('Price/Sale Ratio')
    plt.title('P/S Ratio to Rev Growth (Most Recent)')

    # Axis range
    min_y = min(0, scat.TotalRevenue_Gro.min())
    max_y = max(1, scat.TotalRevenue_Gro.max())
    min_x = min(0, scat.PsRatio.min())
    max_x = max(100, scat.PsRatio.max())

    plt.ylim(min_y, max_y)
    plt.xlim(min_x, max_x)

    # Comp point label
    for i, txt in enumerate(scat.Comp):
        ax.annotate(
            txt,
            (
                scat.PsRatio[i] + (max_x - min_x) * 0.002,             # X offset
                scat.TotalRevenue_Gro[i]                                # Y offset
            )
        )

    # Total Revenue Label
    for m, mc in enumerate(scat.TotalRevenue):
        ax.annotate(
            '$' + str(int(mc/1000000)) + 'm',
            (
                scat.PsRatio[m] + (max_x - min_x) * 0.002,              # x offset
                scat.TotalRevenue_Gro[m] - (max_y - min_y) * 0.025      # y offset
            ),
            size=8
        )

    plt.show()
    plt.tight_layout()

    print(scat)


###############################################################################################
# Cost stats
def cost_stats(rev_df, tickers, start_yr=2018):

    rev_df = rev_df[rev_df.Comp.isin(tickers)]

    fig, ax = plt.subplots(2, 2)
    sns.lineplot(x='Date', y='R&D_pct_Rev', hue='Comp', data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3,
        ax=ax[0, 0]
    ).set_title('R&D percent of Revenue')
    sns.lineplot(x='Date', y='S&M_pct_Rev', hue='Comp', data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3,
        ax=ax[0, 1]
    ).set_title('S&M percent of Revenue')
    sns.lineplot(x='Date', y='Rev_per_R&D', hue='Comp', data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3,
        ax=ax[1, 0]
    ).set_title('Revevenue per R&D')
    sns.lineplot(x='Date', y='Rev_per_S&M', hue='Comp', data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3,
        ax=ax[1, 1]
    ).set_title('Revenue per S&M')
    ax[0, 0].grid()
    ax[0, 1].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    plt.setp(ax[0, 0].get_xticklabels(), rotation=30)
    plt.setp(ax[0, 1].get_xticklabels(), rotation=30)
    plt.setp(ax[1, 0].get_xticklabels(), rotation=30)
    plt.setp(ax[1, 1].get_xticklabels(), rotation=30)
    fig.tight_layout()
    fig.suptitle('Cost Statistics', fontsize=14)
    plt.show()
