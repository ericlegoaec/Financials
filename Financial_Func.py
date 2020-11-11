"""
FUNCTIONS

@author:    Gerard Mazi
@date:      2020-10-30
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import matplotlib.pyplot as plt


'=============================================================='
userid = ''
password = ''
'=============================================================='

driver = webdriver.Chrome(r"chromedriver.exe")
driver.maximize_window()
driver.get('https://login.yahoo.com/')
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@class="phone-no "]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="login-signin"]').click()
time.sleep(1)

driver.find_element_by_xpath('//*[@class="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="login-signin"]').click()
time.sleep(5)

tickers = pd.read_csv('Comps.csv').iloc[:, 0].values.tolist()

for t in range(len(tickers)):

    # Income Statement
    driver.get('https://finance.yahoo.com/quote/' + tickers[t] + '/financials?p=' + tickers[t])
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
    time.sleep(3)

    # Balance Sheet
    driver.get('https://finance.yahoo.com/quote/' + tickers[t] + '/balance-sheet?p=' + tickers[t])
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
    time.sleep(3)

    # Cash Flows
    driver.get('https://finance.yahoo.com/quote/' + tickers[t] + '/cash-flow?p=' + tickers[t])
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
    time.sleep(3)

    # Stats
    driver.get('https://finance.yahoo.com/quote/' + tickers[t] + '/key-statistics?p=' + tickers[t])
    time.sleep(2)
    driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
    time.sleep(2)

driver.quit()
