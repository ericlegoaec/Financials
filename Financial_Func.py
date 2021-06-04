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
from numpy.polynomial.polynomial import polyfit

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
        file['Comp'] = files[f][25:30].replace('_', '').replace('q', '').replace('u', '').replace('a', '')

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
        file['Comp'] = files[f][25:30].replace('_', '').replace('q', '').replace('u', '').replace('a', '')

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

def fin_calc(data, tickers):
    field = [
        'TotalRevenue', 'CostOfRevenue', 'OtherGandA', 'SellingAndMarketingExpense',
        'ResearchAndDevelopment'
    ]

    # Calc year over year growth rate
    data = data[data.Comp.isin(tickers)]
    rev = data.groupby(['Comp', 'Date'])['Value'].sum().reset_index()[['Comp', 'Date']]

    # Calc revenue growth
    for f in field:
        rev_temp = data[data.name == f].groupby(['Comp', 'Date'])['Value'].sum().rename(f).reset_index()
        rev_temp[f + '_Gro'] = rev_temp.groupby('Comp')[f].apply(lambda g: g.pct_change(periods=4))

        rev = pd.merge(rev, rev_temp, how='left', on=['Comp', 'Date'])

    # Calc cost pct of revenue
    rev['S&M_pct_Rev'] = rev.SellingAndMarketingExpense / rev.TotalRevenue
    rev['R&D_pct_Rev'] = rev.ResearchAndDevelopment / rev.TotalRevenue

    # Calc revenue per cost
    rev['Rev_per_S&M'] = rev.TotalRevenue / rev.SellingAndMarketingExpense
    rev['Rev_per_R&D'] = rev.TotalRevenue / rev.ResearchAndDevelopment

    # Gross Profit
    rev = pd.merge(
        rev,
        data[data.name == 'GrossProfit']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .rename('GrossProfit'),
        how='left',
        on=['Comp', 'Date']
    )

    # Operating Profit
    rev = pd.merge(
        rev,
        data[data.name == 'OperatingIncome']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .rename('OperatingIncome'),
        how='left',
        on=['Comp', 'Date']
    )

    # Net Profit
    rev = pd.merge(
        rev,
        data[data.name == 'NetIncome']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .rename('NetIncome'),
        how='left',
        on=['Comp', 'Date']
    )

    # Margin Calc
    rev['Gross_Prof_Marg'] = rev.GrossProfit / rev.TotalRevenue
    rev['Ops_Prof_Marg'] = rev.OperatingIncome / rev.TotalRevenue
    rev['Net_Prof_Marg'] = rev.NetIncome / rev.TotalRevenue

    # Merge shares outstanding
    rev = pd.merge(
        rev,
        data[data.name == 'DilutedAverageShares']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .replace(to_replace=0, method='ffill')
            .rename('Shares'),
        how='left',
        on=['Comp', 'Date']
    )

    # Merge Free Cash Flows
    rev = pd.merge(
        rev,
        data[data.name == 'FreeCashFlow']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .rename('FCF'),
        how='left',
        on=['Comp', 'Date']
    )

    # Calc Free Cash Flows per share
    rev['FCF_Share'] = rev.FCF / rev.Shares

    # Merge balance sheet cash
    rev = pd.merge(
        rev,
        data[data.name == 'CashCashEquivalentsAndShortTermInvestments']
            .groupby(['Comp', 'Date'])['Value']
            .sum()
            .rename('Cash'),
        how='left',
        on=['Comp', 'Date']
    )

    return rev


################################################################################################
# Group Revenue Growth Trends
def group_trend(rev_df, tickers, start_yr=2010):

    rev_df = rev_df[rev_df.Comp.isin(tickers)]
    rev_df2 = pd.merge(
        rev_df.groupby('Comp')['Date'].max().reset_index(),
        rev_df[['Date', 'Comp', 'TotalRevenue_Gro']],
        how='left',
        on=['Date', 'Comp']
    )

    plt.figure()
    sns.lineplot(
        x='Date',
        y='TotalRevenue_Gro',
        hue='Comp',
        data=rev_df[rev_df.Date > str(start_yr)],
        linewidth=3
    ).set_title('Revenue Growth Trend')
    plt.axhline(0, ls='--', c='black', linewidth=2)
    for i, c in enumerate(rev_df2.Comp):
        plt.annotate(
            c,
            (
                rev_df2.Date[i],
                rev_df2.TotalRevenue_Gro[i]
            )
        )
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
    ax2.axhline(0, ls='--', c='black', linewidth=2)

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Total Revenue (millions)')
    ax2.set_ylabel('Growth Rate (YoY)')
    plt.title(ticker +  ' Revenue Growth (YoY)')
    plt.grid(True)
    plt.show()

    print(rev_stats[['Date', 'TotalRevenue', 'TotalRevenue_Gro']])

################################################################################################
# Price/Sales Group Trend
def ps_trend(data, tickers, start_yr=2010):

    data = data[data.Comp.isin(tickers)]
    data = data.loc[(data.name == 'PsRatio') & (data.Date >= str(start_yr)), :]
    data2 = data[data.Date == data.Date.max()].groupby(['Comp'])['Value'].sum().reset_index()

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
    for i, c in enumerate(data2.Comp):
        plt.annotate(
            c,
            (
                data.Date.max(),
                data2.Value[i]
            )
        )
    plt.grid()
    plt.show()

    print(data.groupby(['Date', 'Comp'])['Value'].sum().unstack())


################################################################################################
# Price/Sales Group Scatter Plot

def ps_scat(stats_df, rev_df, tickers, type='bubble'):
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

    if type == 'bubble':
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

    elif type == 'simple':


        plt.figure()
        ax = plt.subplot(111)
        plt.grid(True)
        ax.plot([0, 1], [0, 1], color='red', transform=ax.transAxes, linewidth=0.5)
        ax.scatter(x=scat.PsRatio, y=scat.TotalRevenue_Gro, alpha=0.5, s=30)
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
                    scat.PsRatio[i] + (max_x - min_x) * 0.002,     # X offset
                    scat.TotalRevenue_Gro[i]                        # Y offset
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

####################################################################################################
# FCF / Share Trend all Comps
def fcf_sh_trend(data, tickers, start_yr=2010):

    fin_df = data[data.Comp.isin(tickers)]
    fin_df2 = data[data.Date == data.Date.max()].groupby(['Comp'])['FCF_Share'].sum().reset_index()

    plt.figure()
    sns.lineplot(
        x='Date',
        y='FCF_Share',
        hue='Comp',
        data=fin_df[fin_df.Date > str(start_yr)],
        linewidth=3
    ).set_title('Free Cash Flows per Share Trend')
    plt.grid()
    plt.axhline(0, ls='--', c='black', linewidth=2)
    for i, c in enumerate(fin_df2.Comp):
        plt.annotate(
            c,
            (
                fin_df.Date.max(),
                fin_df2.FCF_Share[i]
            )
        )
    plt.show()

    print(fin_df.groupby(['Date', 'Comp'])['FCF_Share'].sum().unstack()[str(start_yr):])

####################################################################################################
# FCF Trend on individual comps
def fcf_comp_trend(data, ticker, range=60):

    # Source Data
    fcf_stats = data.loc[data.Comp == ticker, ['Date', 'Cash', 'FCF_Share']]

    # Format to Millions
    fcf_stats['Cash'] = fcf_stats.Cash / 1000000

    # Time frame
    fcf_stats = fcf_stats.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(fcf_stats.Date, fcf_stats.Cash, width=80, color='Lightgray', label='Cash')
    ax2.plot(fcf_stats.Date, fcf_stats['FCF_Share'], 'o-', color='black', label='FCF per Share', linewidth=3)

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Cash (millions)')
    ax2.set_ylabel('Free Cash Flows per Share')
    plt.title(ticker + ' Free Cash Flows')
    plt.axhline(0, ls='--', c='black', linewidth=2)
    plt.grid(True)
    align_yaxis(ax1, ax2)
    plt.show()

    print(fcf_stats)


#################################################################################################
# For Dual Axis share y=0
def align_yaxis(ax1, ax2):
    y_lims = np.array([ax.get_ylim() for ax in [ax1, ax2]])

    # force 0 to appear on both axes, comment if don't need
    y_lims[:, 0] = y_lims[:, 0].clip(None, 0)
    y_lims[:, 1] = y_lims[:, 1].clip(0, None)

    # normalize both axes
    y_mags = (y_lims[:,1] - y_lims[:,0]).reshape(len(y_lims),1)
    y_lims_normalized = y_lims / y_mags

    # find combined range
    y_new_lims_normalized = np.array([np.min(y_lims_normalized), np.max(y_lims_normalized)])

    # denormalize combined range to get new axes
    new_lim1, new_lim2 = y_new_lims_normalized * y_mags
    ax1.set_ylim(new_lim1)
    ax2.set_ylim(new_lim2)


#################################################################################################
# Gross Profit Margin Individual Comp

def gross_prof(data, ticker, range=60):

    # Source Data
    gross_stats = data.loc[data.Comp == ticker, ['Date', 'GrossProfit', 'Gross_Prof_Marg']]

    # Format to Millions
    gross_stats['GrossProfit'] = gross_stats.GrossProfit / 1000000

    # Time frame
    gross_stats = gross_stats.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(gross_stats.Date, gross_stats.GrossProfit, width=80, color='Lightgray', label='Gross Profit')
    ax2.plot(gross_stats.Date, gross_stats['Gross_Prof_Marg'], 'o-', color='black', label='Gross Profit Margin', linewidth=3)

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Gross Profit (millions)')
    ax2.set_ylabel('Gross Profit Margin')
    plt.title(ticker + ' Gross Profit')
    plt.grid(True)
    plt.axhline(0, ls='--', c='black', linewidth=2)

    align_yaxis(ax1, ax2)
    plt.show()

#################################################################################################
# Operating Profit Margin Individual Comp

def ops_prof(data, ticker, range=60):

    # Source Data
    ops_stats = data.loc[data.Comp == ticker, ['Date', 'OperatingIncome', 'Ops_Prof_Marg']]

    # Format to Millions
    ops_stats['OperatingIncome'] = ops_stats.OperatingIncome / 1000000

    # Time frame
    ops_stats = ops_stats.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(ops_stats.Date, ops_stats.OperatingIncome, width=80, color='Lightgray', label='Operating Profit')
    ax2.plot(ops_stats.Date, ops_stats['Ops_Prof_Marg'], 'o-', color='black', label='Operating Profit Margin', linewidth=3)

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Operating Profit (millions)')
    ax2.set_ylabel('Operating Profit Margin')
    plt.title(ticker + ' Operating Profit')
    plt.grid(True)
    plt.axhline(0, ls='--', c='black', linewidth=2)

    align_yaxis(ax1, ax2)
    plt.show()

#################################################################################################
# Net Profit Margin Individual Comp

def net_prof(data, ticker, range=60):

    # Source Data
    net_stats = data.loc[data.Comp == ticker, ['Date', 'NetIncome', 'Net_Prof_Marg']]

    # Format to Millions
    net_stats['NetIncome'] = net_stats.NetIncome / 1000000

    # Time frame
    net_stats = net_stats.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(net_stats.Date, net_stats.NetIncome, width=80, color='Lightgray', label='Net Profit')
    ax2.plot(net_stats.Date, net_stats['Net_Prof_Marg'], 'o-', color='black', label='Net Profit Margin', linewidth=3)

    ax2.legend(loc='upper left')

    ax1.set_ylabel('Net Profit (millions)')
    ax2.set_ylabel('Net Profit Margin')
    plt.title(ticker + ' Net Profit')
    plt.grid(True)
    plt.axhline(0, ls='--', c='black', linewidth=2)

    align_yaxis(ax1, ax2)
    plt.show()

######################################################################################################################
# KPI Group Trend on several comps

def kpi_group_trend(tickers, start_yr=2010):

    # load data
    data = pd.read_csv('kpi.csv', parse_dates=['Date'])

    # target comps and KPI
    data = data.loc[(data.Comp.isin(tickers)) & (data.Date >= str(start_yr)), :]
    data2 = data[data.Date == data.Date.max()].groupby(['Comp'])['Value'].sum().reset_index()

    plt.figure()
    sns.lineplot(
        x='Date',
        y='Value',
        hue='Comp',
        data=data,
        linewidth=3
    )
    plt.ylabel(data.KPI.values[0])
    plt.title(data.KPI.values[0] + ' Trend')
    for i, c in enumerate(data2.Comp):
        plt.annotate(
            c,
            (
                data.Date.max(),
                data2.Value[i]
            )
        )
    plt.grid()
    plt.show()

    print(data.groupby(['Date', 'Comp'])['Value'].sum().unstack())

######################################################################################################################
# KPI Growth Trend on several comps

def kpi_growth_trend(tickers, kpi, start_yr=2010):

    # load data
    data = pd.read_csv('kpi.csv', parse_dates=['Date'])

    # target comps and KPI
    data = data.loc[(data.Comp.isin(tickers)) & (data.KPI == kpi), :]

    gro = pd.DataFrame({'Comp': [], 'Date': [], 'KPI': [], 'Value': [], 'Growth': []})

    # Calc year over year growth rate
    for t in tickers:
        gro_temp = data[data.Comp == t].sort_values(by='Date')
        gro_temp['Growth'] = gro_temp['Value'].pct_change(periods=4)

        gro = pd.concat([gro, gro_temp], ignore_index=True)

    gro = gro[gro.Date >= str(start_yr)]
    gro2 = gro[gro.Date == gro.Date.max()].groupby(['Comp'])['Growth'].sum().reset_index()

    plt.figure()
    sns.lineplot(
        x='Date',
        y='Growth',
        hue='Comp',
        data=gro,
        linewidth=3
    )
    plt.ylabel(kpi)
    plt.title(kpi + ' Growth Trend')
    plt.axhline(0, ls='--', c='black', linewidth=2)
    for i, c in enumerate(gro2.Comp):
        plt.annotate(
            c,
            (
                gro.Date.max(),
                gro2.Growth[i]
            )
        )
    plt.grid()
    plt.show()

    print(gro.groupby(['Date', 'Comp'])['Growth'].sum().unstack())

######################################################################################################################
# KPI Vintage analysis

def kpi_vintage_trend(tickers, kpi):

    # load data
    data = pd.read_csv('kpi.csv', parse_dates=['Date'])

    # target comps and KPI
    data = data.loc[(data.Comp.isin(tickers)) & (data.KPI == kpi), :].sort_values(by=['Comp', 'Date'])

    vin = pd.DataFrame({'Comp': [], 'Value': []})

    for t in tickers:
        vin_temp = data.loc[data.Comp == t, ['Comp', 'Value']].reset_index()[['Comp', 'Value']]
        vin = pd.concat([vin, vin_temp], ignore_index=False)

    vin = vin.reset_index()

    plt.figure()
    sns.lineplot(
        x='index',
        y='Value',
        hue='Comp',
        data=vin,
        linewidth=3
    )
    plt.ylabel(kpi)
    plt.xlabel('Quarters')
    plt.title(kpi + ' Vintage Trend')
    plt.grid()
    plt.show()


#################################################################################################
# KPIs Individual Comp

def kpi_comp_trend(ticker, kpi, range=60):

    # load data
    data = pd.read_csv('kpi.csv', parse_dates=['Date'])

    # Isolate target kpi and comp
    data = data.loc[(data.Comp == ticker) & (data.KPI == kpi), ['Date', 'Value']].sort_values(by='Date')

    # Calc growth rate
    data['Growth'] = data.Value.pct_change(periods=4)

    # Time frame
    data = data.tail(range)

    # Plot
    plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()
    ax1.bar(data.Date, data['Value'], width=80, color='Lightgray', label=kpi)
    ax2.plot(data.Date, data['Growth'], 'o-', color='black', label='YoY Growth', linewidth=3)

    ax2.legend(loc='upper left')

    ax1.set_ylabel(kpi)
    ax2.set_ylabel('Growth')
    plt.title(ticker + ' ' + kpi)
    plt.grid(True)
    plt.axhline(0, ls='--', c='black', linewidth=2)

    align_yaxis(ax1, ax2)
    plt.show()