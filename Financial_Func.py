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

###############################################################################################
# Merge financials

# Import files
def import_fin():
    files = glob.glob('C:/Users/gerard/Downloads/*')
    financials = pd.DataFrame({'Comp': [], 'name': [], 'Date': [], 'Value': []})

    for f in range(len(files)):
        file = pd.read_csv(files[f])
        file['Comp'] = files[f][26:30].replace('_', '')
        file = pd.melt(file, id_vars=['Comp', 'name'], var_name='Date', value_name='Value')

        financials = pd.concat([financials, file], axis=0, ignore_index=True)




