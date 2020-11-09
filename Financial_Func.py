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

#roles = pd.read_pickle('store_roles.pkl')

'=============================================================='
userid = ''
password = ''
'=============================================================='

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://login.yahoo.com/')
driver.maximize_window()
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@class="phone-no "]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="login-signin"]').click()
time.sleep(1)

driver.find_element_by_xpath('//*[@class="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="login-signin"]').click()
time.sleep(5)

tickers = ['NOW']

# Income Statement
driver.get('https://finance.yahoo.com/quote/' + tickers[0] + '/financials?p=' + tickers[0])
time.sleep(2)
driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
time.sleep(2)

# Balance Sheet
driver.get('https://finance.yahoo.com/quote/' + tickers[0] + '/balance-sheet?p=' + tickers[0])
time.sleep(2)
driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
time.sleep(2)

# Cash Flows
driver.get('https://finance.yahoo.com/quote/' + tickers[0] + '/cash-flow?p=' + tickers[0])
time.sleep(2)
driver.find_element_by_xpath('//*[@class="P(0px) M(0px) C($linkColor) Bd(0px) O(n)"]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
time.sleep(2)

# Stats
driver.get('https://finance.yahoo.com/quote/' + tickers[0] + '/key-statistics?p=' + tickers[0])
time.sleep(2)
driver.find_element_by_xpath('//*[@class="Pos(r) smplTblTooltip C($linkColor) BdStart Bdc($seperatorColor) Pstart(10px) Mstart(10px)"]').click()
time.sleep(2)

driver.quit()
