import argparse, os, time
import csv
import datetime
import json
import numpy as np
import operator
import pandas as pd
import re
import requests
import string
import sys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from telnetlib import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import xml.etree.ElementTree as ET
import json
import requests
from datetime import timedelta, date

# Please set the search start/end date here.
SearchStartDate = date(2020, 3, 1)
SearchEndDate = date(2020, 4, 1)
dirPath = 'C:/Users/Muffin/Downloads/'

# add chrome directory and open chrome browser
path_to_chromedriver = dirPath + 'chromedriver'
fileType = 'sold'
fileSource = 'jaguar'
pd.to_datetime(SearchStartDate).strftime('%Y-%m-%d').replace("-", "")
dateRange = pd.to_datetime(SearchStartDate).strftime('%m-%d-%Y').replace("-", "/") + " - " + pd.to_datetime(
    SearchEndDate).strftime('%m-%d-%Y').replace("-", "/")
new_dir = dirPath + fileSource + '-' + fileType + '-' + dateRange
path = dirPath

files = os.listdir(dirPath)
if new_dir.split('/')[-1] not in files:
    os.makedirs(new_dir)
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': new_dir}
options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(executable_path=r'C:/Program Files/chromedriver/chromedriver.exe')

url = 'url_here'
browser.get(url)


def login():
    # enter username and password and submit
    username = browser.find_element_by_name("username")
    password = browser.find_element_by_name("password")
    username.send_keys('username')
    password.send_keys('password')
    browser.find_element_by_xpath("//button[@class='login-btn btn flex convertcase']").click()
    time.sleep(5)


def setup():
    # Click sidebar
    browser.find_element_by_xpath("//a[@class='sidebar-toggle']").click()
    time.sleep(5)
    # Click for search properties
    browser.find_element_by_xpath("//i[@title='Search Properties']").click()
    time.sleep(5)
    # Click for advanced search
    browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/section/div/div[2]/div/div/div[1]/div[2]/div/a[1]/span[2]").click()
    time.sleep(5)

    # Unlick All active
    allActiveButton = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]")
    browser.execute_script("arguments[0].click();", allActiveButton)


def clickSold():
    # Click "Sold"
    soldButton = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[5]/div[3]")
    browser.execute_script("arguments[0].click();", soldButton)


def clickContract():
    # Click "Contract"
    contractButton = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]/div[2]")
    browser.execute_script("arguments[0].click();", contractButton)


# #### When it's for contract, please modify the function. Uncomment # Status == Contract.
def scrape(neighborhood, startdate, enddate):
    time.sleep(15)

    # Status == Sold, PLEASE UNCOMMENT THIS PART WHEN STATUS IS SOLD, AND COMMENT CONTRACT 
    soldSearchDate = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[3]/div/div/date-range-picker/div/div/input")
    browser.execute_script("arguments[0].click();", soldSearchDate)

    soldStartDate = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[3]/div/div/date-range-picker/div/div[2]/div[1]/div[2]/div[1]/input")
    browser.execute_script("arguments[0].click();", soldStartDate)

    soldEndDate = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[3]/div/div/date-range-picker/div/div[2]/div[1]/div[2]/div[2]/input")
    browser.execute_script("arguments[0].click();", soldEndDate)

    soldStartDate.clear()
    soldStartDate.send_keys(startdate)
    soldEndDate.clear()
    soldEndDate.send_keys(enddate)

    soldSearchDateApply = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[3]/div/div/date-range-picker/div/div[2]/div[2]/button[1]")
    browser.execute_script("arguments[0].click();", soldSearchDateApply)

    #     # Status == Contract, PLEASE UNCOMMENT THIS PART WHEN STATUS IS CONTRACTED, AND COMMENT SOLD
    #     contractSearchDate = browser.find_element_by_xpath("//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/date-range-picker/div/div/input")
    #     browser.execute_script("arguments[0].click();", contractSearchDate)

    #     contractStartDate = browser.find_element_by_xpath("//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/date-range-picker/div/div[2]/div[1]/div[2]/div[1]/input")
    #     browser.execute_script("arguments[0].click();", contractStartDate)
    #     contractEndDate =  browser.find_element_by_xpath("//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/date-range-picker/div/div[2]/div[1]/div[2]/div[2]/input")
    #     browser.execute_script("arguments[0].click();", contractEndDate)

    #     contractStartDate.clear()
    #     contractStartDate.send_keys(startdate)
    #     contractEndDate.clear()
    #     contractEndDate.send_keys(enddate)

    #     contractSearchDateApply = browser.find_element_by_xpath("//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/date-range-picker/div/div[2]/div[2]/button[1]")
    #     browser.execute_script("arguments[0].click();", contractSearchDateApply)

    # Neighborhoods
    if neighborhood == "manhattan_u":
        # Click dropdown for neighborhoods
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[13]/div[2]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # West Side/East Side Manhattan
    if neighborhood == "manhattan_we":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[15]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # Downtown Manhattan
    if neighborhood == "manhattan_d":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[7]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # Queens
    if neighborhood == "queens":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[19]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

        # Brooklyn
    if neighborhood == "brooklyn":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[17]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # Staten Island
    if neighborhood == "staten_island":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[23]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # The Bronx
    if neighborhood == "bronx":
        dropDown = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
        browser.execute_script("arguments[0].click();", dropDown)
        button = browser.find_element_by_xpath(
            "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[21]/div[3]")
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # Click on search
    Search = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/section/div/div[1]/div[3]/div[2]/div[2]/button[1]")
    browser.execute_script("arguments[0].click();", Search)
    time.sleep(10)

    # Export the listings
    # Check "Check All" to select all data
    checkAllButton = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/div[2]/div/div[5]/div/div[2]/div[1]/div[1]")
    browser.execute_script("arguments[0].click();", checkAllButton)
    # Side bar to export
    sideBar = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/div[2]/div/div[5]/div/div[1]/div[2]/ul/li[6]/a")
    browser.execute_script("arguments[0].click();", sideBar)
    # Click export
    clickExport = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/div[2]/div/div[5]/div/div[1]/div[2]/ul/li[6]/div/div[2]/ul/li[3]/a/span")
    browser.execute_script("arguments[0].click();", clickExport)
    # Click CSV export
    clickCSVExport = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/div[2]/div/div[5]/div/div[1]/div[2]/ul/li[6]/div/div[2]/ul/li[3]/div/a[1]")
    browser.execute_script("arguments[0].click();", clickCSVExport)
    # Click "select all" option
    clickSelectAll = browser.find_element_by_xpath(
        "//*[@id=\"exportGridViewModal\"]/div/div/div/div[2]/div/div[1]/button[1]")
    browser.execute_script("arguments[0].click();", clickSelectAll)
    # Click Export to download the listings
    downloadExport = browser.find_element_by_xpath(
        "//*[@id=\"exportGridViewModal\"]/div/div/div/div[2]/div/div[2]/button")
    browser.execute_script("arguments[0].click();", downloadExport)

    # Back to Advanced Search
    backToSearch = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/div[2]/div/div[5]/div/div[1]/div[2]/ul/li[5]/a")
    browser.execute_script("arguments[0].click();", backToSearch)

    time.sleep(5)

    # Clear the neighborhood items
    dropDown = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
    browser.execute_script("arguments[0].click();", dropDown)
    dropDownClear = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/button")
    browser.execute_script("arguments[0].click();", dropDownClear)
    dropDown = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[1]")
    browser.execute_script("arguments[0].click();", dropDown)


def goBack():
    sideBar = browser.find_element_by_xpath("//*[@id=\"appBody\"]/div[3]/header/nav/div/a")
    browser.execute_script("arguments[0].click();", sideBar)
    searchBar = browser.find_element_by_xpath("//*[@id=\"appBody\"]/div[3]/aside/section/div[1]/div/ul/li[2]/a[1]")
    browser.execute_script("arguments[0].click();", searchBar)
    time.sleep(3)
    allActiveButton2 = browser.find_element_by_xpath(
        "//*[@id=\"content\"]/div[1]/div[2]/section/div/div[2]/div/div/div[1]/div[2]/div/a[1]/span[2]")
    browser.execute_script("arguments[0].click();", allActiveButton2)
    time.sleep(3)
    allActiveButton2 = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]")
    browser.execute_script("arguments[0].click();", allActiveButton2)
    soldButton2 = browser.find_element_by_xpath(
        "//*[@id=\"advanced-contents\"]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[5]/div[2]")
    browser.execute_script("arguments[0].click();", soldButton2)


def time_generater(start_date, end_date, interval):
    tmp_list = []
    time_log = int((end_date - start_date).days)
    rounds = time_log // (interval)
    remainder = time_log % (interval)
    a = start_date
    for i in range(rounds):
        b = a + timedelta(days=interval - 1)
        tmp_list.append([a.strftime("%m/%d/%Y"), b.strftime("%m/%d/%Y")])
        a = b + timedelta(days=1)
    tmp_list.append([a.strftime("%m/%d/%Y"), (a + timedelta(days=remainder)).strftime("%m/%d/%Y")])
    return tmp_list


def dict_generater(neighbors_days, start_date, end_date):
    neighbors = {}
    for key in neighbors_days:
        neighbors[key] = time_generater(start_date, end_date, neighbors_days[key])
    return neighbors


# #### Set start date and end date, also date duration for each neighborhoods.
start_date = SearchStartDate
end_date = SearchEndDate
neighbors_days = {'staten_island': 10, 'bronx': 10, 'brooklyn': 5, 'manhattan_we': 3, 'manhattan_u': 3,
                  'manhattan_d': 3, 'queens': 10}

neighbors = dict_generater(neighbors_days, start_date, end_date)

finished_neighbors = set()

# ### ----------- Scrape data, run again for those not scrapped previously. -------------

login()
setup()
clickSold()

# Run the scraper.
for area, dates in neighbors.items():
    for date in dates:
        key = (area, date[0], date[1])
        if key not in finished_neighbors:
            print("scrapping", *key)
            try:
                scrape(area, date[0], date[1])
            except Exception:
                goBack()
                print("###### CRASH #######", *key)
            finished_neighbors.add(key)
        else:
            print("already scrapped", *key)

# fileType = 'incontract'
os.chdir(path + "nyc")
files = os.listdir(path + "nyc")
print(files)
len(files)
first = 0
out = open(files[first])
data = pd.read_csv(out, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
data_column = list(data)
columns = []
for col in data_column:
    columns.append(col.replace(' ', '').replace(' ', ''))
data.columns = columns
for index in range(first + 1, len(files)):
    out = open(files[index], 'rb')
    df = pd.read_csv(out, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    data_column = list(df)
    columns = []
    for col in data_column:
        columns.append(col.replace(' ', '').replace(' ', ''))
    df.columns = columns
    data = pd.concat([data, df], axis=0, ignore_index=True)
    # print data
    print("Index = " + str(index))
    print(files[index])
data = data.rename(columns={'SoldDate': 'ClosingDate'})
data = data.replace("---", "")
data = data.fillna("")
for i in list(data):
    data[i] = data[i].astype(str).str.encode("ascii", "ignore").str.decode('utf-8')
data = data.drop_duplicates()
if fileType == 'active':
    dateType = "Listed"
if fileType == 'incontract':
    dateType = "ContractSigned"
if fileType == 'sold':
    dateType = "ClosingDate"
if fileSource == 'jaguar':
    data['ListedDate'] = pd.to_datetime(data['ListedDate'])
    data['ContractSigned'] = pd.to_datetime(data['ContractSigned'])
    data['ClosingDate'] = pd.to_datetime(data['ClosingDate'])
    data = data[
        (data[dateType] > ((pd.to_datetime(SearchStartDate) - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))) & (
                    data[dateType] < (
                (pd.to_datetime(SearchEndDate) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')))]

with open(path + fileSource + "-" + fileType + "-" + dateRange + "-concatenated.csv", 'w') as outfile:
    data.to_csv(outfile, sep=',')

# Format Address
data = pd.read_csv(path + fileSource + "-" + fileType + "-" + dateRange + "-concatenated.csv", dtype='unicode')
data['input_string'] = data['Address'] + ', NY, ' + data['Zipcode'].map(str)
data['formatted_address'] = ''
data['Lat'] = ''
data['Lng'] = ''

df = list(data['input_string'])
addList = []
latList = []
lonList = []
for index in range(len(data)):
    try:
        jsonData = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address=' + df[index] + '&key=apikey')
        jsonData = jsonData.content
        jsonData = json.loads(jsonData)
        data.loc[index, 'formatted_address'] = jsonData['results'][0]['formatted_address']
        data.loc[index, 'Lat'] = jsonData['results'][0]['geometry']['location']['lat']
        data.loc[index, 'Lng'] = jsonData['results'][0]['geometry']['location']['lng']
    except:
        ("No Address")
    print("google api progress : " + str(index) + "/" + str(len(data)))

### Part Two
len(data[data['formatted_address'].isnull()])

merge = data
merge['formatted_address2'] = merge['formatted_address']
merge['formatted_address2'][merge['formatted_address2'].isnull()] = merge['input_string'][
    merge['formatted_address2'].isnull()]
merge['Unit2'] = merge['Unit'].str.replace(" ", "").str.replace("NOAPT", "").str.upper().fillna("")

merge.to_csv('combined.csv')
