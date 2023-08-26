from lxml import html
import requests
import re
import csv
from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

def html_parse_tree(url):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.page_load_strategy = 'normal' 
    chrome_path = "./bin/chromedriver.exe" #ChromeDriverManager()#.install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=options, service=chrome_service) 
    #driver.implicitly_wait(5)
    driver.get(url) 
    return html.fromstring(driver.page_source)

def xpath_parse(tree, xpath):
    result = tree.xpath(xpath)
    return result

def regex_strip_array(array):
    for i in range(0, len(array)):
        array[i] = regex_strip_string(array[i]).strip()
    return array

def regex_strip_string(string):
    string = re.sub('\n', '', string).strip()
    string = re.sub('\r', '', string).strip()
    string = re.sub('\t', '', string).strip()
    return string

def format_spacing(max_spacing, variable):
    spacing_count = max_spacing - len(variable)
    output = ''
    for i in range(0, spacing_count):
        output += ' '
    return output

def fraction_stats(string):
    string = string.replace('(', '')
    string = string.replace(')', '')
    return string.split('/')

def add2csv(array, filename):
    with open(filename, 'a',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(array)

def array2csv(array, filename):
    with open(filename, "w+",newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter = ',')
        csvWriter.writerows(array)