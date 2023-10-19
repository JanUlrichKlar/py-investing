#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import shutil
from bs4 import BeautifulSoup
import requests
from lxml import html
from bs4 import BeautifulSoup
from lxml import html
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


def get_historic(instrument):
    print(instrument)
    if instrument['type'] == 'stock':
        stock_historic(instrument)
    if instrument['type'] == 'etf':
        etf_historic(instrument)


def stock_historic(stock: dict, country=None):
    # set chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url_base = stock['url']
    driver.get(url_base)
    print(driver)
    search_date1 = Wait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'dtDate1')))
    search_date2 = Wait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'dtDate2')))
    search_boerse = Wait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'strBoerse')))
    driver.implicitly_wait(2)
    search_date1.send_keys('01.02.2023')
    search_date2.send_keys('03.02.2023')
    search_boerse.send_keys('FSE')
    print(search_date1, search_date2)

    button = driver.find_element(By.XPATH, '/html/body/main/section[2]/div/article/form/div/div[10]/button')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    #print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table')[1]
    print(len(table))
    #print(table[1])
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    output_rows = [x for x in output_rows if x != []]
    #print(output_rows)

    historic_data = pd.DataFrame(np.array(output_rows),
                                 columns=['date', 'open', 'close', 'high', 'low', 'volume'])

    historic_data['date'] = pd.to_datetime(historic_data['date'], format='%d.%m.%Y')

    # as in german comma separates decimal places the data must be corrected
    # also sometimes no value exists, so it is set to 0
    for price in ['open', 'close', 'high', 'low']:
        historic_data[price] = historic_data[price].str.replace('-', '0', regex=False)
        historic_data[price] = historic_data[price].str.replace(',', '.', regex=False).astype(float)
    historic_data['volume'] = historic_data['volume'].str.replace('-', '0', regex=False)
    historic_data['volume'] = historic_data['volume'].str.replace('.', '', regex=False).astype(float)

    print(historic_data)

    driver.close()


def etf_historic(etf: dict, country=None):
    # set chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url_base = etf['url']
    driver.get(url_base)
    print(driver)

    # close pop-up accept button
    # switch frame
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sp_message_iframe_735274"]'))
    # locate accept button
    accept_button = Wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                          '//*[@id="notice"]/div[3]/div[2]/button')))
    # click accept button
    driver.execute_script("arguments[0].click();", accept_button)
    # switch back to main frame
    driver.switch_to.default_content()

    url = 'https://www.finanzen.net/ajax/FundController_HistoricPriceListRedesign/ishares-sp-500-utilities-sector-etf-ie00b4kbbd01/STU/07.12.2022_15.12.2022'

    r = requests.post(url_base)
    print(r.request.url)
    print(r.request.body)
    print(r.request.headers)
    # print(r.text)
    soup = BeautifulSoup(r.content, 'lxml')
    print(soup)


    search_date1 = Wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                          '//*[@id="maturityDateTrigger"]/div[1]/div')))
    search_date2 = Wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maturityDateTrigger"]/div[2]/div')))
    search_boerse = Wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="historic-prices-stock-market"]')))


    driver.implicitly_wait(2)
    driver.execute_script("arguments[0].scrollIntoView(true);", search_date1)
    select = Select(Wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="historic-prices-stock-market"]'))))
    select.select_by_value('FSE')

    #search_boerse.send_keys('FSE')
    driver.execute_script("arguments[0].style.display = 'block';", search_date1)
    driver.execute_script("arguments[0].style.display = 'block';", search_date2)

    driver.execute_script("arguments[0].value = arguments[1]", search_date1, "01.02.2023")
    driver.execute_script("arguments[0].value = arguments[1]", search_date2, "03.02.2023")
    #search_date1.click()
    # search_date1.clear()
    # search_date1.send_keys('01.02.2023')
    # search_date2.send_keys('03.02.2023')

    print(search_date1, search_date2)

    button = driver.find_element(By.XPATH, '//*[@id="request-historic-price"]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    # print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table')
    #print(len(table))
    #print(table)
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    output_rows = [x for x in output_rows if x != []]
    # print(output_rows)

    historic_data = pd.DataFrame(np.array(output_rows),
                                 columns=['date', 'open', 'close', 'high', 'low', 'volume'])

    historic_data['date'] = pd.to_datetime(historic_data['date'], format='%d.%m.%Y')

    # as in german comma separates decimal places the data must be corrected
    # also sometimes no value exists, so it is set to 0
    for price in ['open', 'close', 'high', 'low']:
        historic_data[price] = historic_data[price].str.replace('-', '0', regex=False)
        historic_data[price] = historic_data[price].str.replace(',', '.', regex=False).astype(float)
    historic_data['volume'] = historic_data['volume'].str.replace('-', '0', regex=False)
    historic_data['volume'] = historic_data['volume'].str.replace('.', '', regex=False).astype(float)

    print(historic_data)

    driver.close()



def load_xls(sec_dict):
    """
    Function to download *.xls from ishares.com
    As the download xls seems corrupt it is
    converted to an *.xlsx
    """
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": r"D:\OneDrive\pyprojects\etf_composition\data\vanguard\\",  # IMPORTANT - ENDING SLASH V IMPORTANT
             "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)
    #chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(sec_dict['href'])
    print(sec_dict['href'])
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//europe-core-download-button/button")))
    button = driver.find_elements_by_xpath("//europe-core-download-button/button")
    driver.execute_script("arguments[0].click();", button[2])
    os.chdir('./data/vanguard')
    curr_path = os.path.abspath(os.getcwd())
    file = ''
    while file == '':
        for file in glob.glob('Aufschlüsselung*.xlsx'):
            print(file)
    file_new = sec_dict['ticker'] + '_' + file.split('-')[-1][1:]
    print(file_new)
    shutil.copy(os.path.join(curr_path, file), os.path.join(curr_path, file_new))
    print(os.listdir())
    os.remove(os.path.join(curr_path, file))
