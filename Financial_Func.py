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

