import time 
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

# The following function requires you to have chrome installed on your computer

## atpurl = https://www.atptour.com/en/scores/current/us-open/560/daily-schedule
## date expected format is YYYY-MM-DD
def generate_y_rows(playersfile, atpurl, date, outputfile): 
    #####################
    ### Retrieving ATP data thanks to selenium
    #####################
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.page_load_strategy = 'normal' 
    chrome_path = "./bin/chromedriver.exe" #ChromeDriverManager()#.install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)
    #atpurl = "https://www.atptour.com/en/scores/current/us-open/560/daily-schedule"
    driver.get(atpurl) 
    bs_atp = bs(driver.page_source, "html.parser")

    # Getting players list from page source code
    table = bs_atp.find('div', attrs={'class':"sectioned-day-tables"}).find_all('td',attrs={'class':'day-table-name'})
    players=[]
    playersedited=[]
    matchplayers=[]
    for torototo in table:
        bala = torototo.find('a')
        players.append(bala.get('data-ga-label'))

    # Transformation to fit our database name (full name, first name only first letter then .)
    # example : Rodionov J.
    [playersedited.append(x.split(' ')[1] +" "+ x.split(' ')[0][0] + ".") for x in players]


    # Making it 2 dim
    # [['Bagnis F.', 'Vandecasteele Q.'],
    #  ['Bouchard E.', 'Hui K.']]
    for i in range(0, len(playersedited), 2):
        matchplayers.append([playersedited[i], playersedited[i+1]])

    #####################
    ### Building y row
    #####################
    players = pd.read_csv("./data/players.csv")

    ## setting up a dataframe with expected column
    col_datas=[]
    for col in players.columns:
        col_datas.append("player1_"+ col)  

    for col in players.columns:
        col_datas.append("player2_"+ col)  

    datas=pd.DataFrame(columns=col_datas)

    for pp in matchplayers:
        if players[players.name==pp[0]].shape[0] == 1:
            p1 = (players[players.name==pp[0]]).values.tolist()[0]
        else:
            dfp1 = (players[players.name==pp[0]]).copy(deep=True) # copy is to avoid the settingwithcopy warning on loc
            dfp1.loc[0,"name"] = pp[0]
            p1 = dfp1.values.tolist()[0]

        if players[players.name==pp[1]].shape[0] == 1:
            p2 = players[players.name==pp[1]].values.tolist()[0]
        else:
            dfp2 = (players[players.name==pp[1]]).copy(deep=True) # copy is to avoid the settingwithcopy warning on loc
            dfp2.loc[0,"name"] = pp[1]
            p2 = dfp2.values.tolist()[0] 

        data = p1 + p2
        datas.loc[len(datas)] = data
    return datas

## need to add
# date
# tournament info (name, location tournament, series, Court, surface, round if possible, best of )
atpurl = "https://www.atptour.com/en/scores/current/us-open/560/daily-schedule"
playersfile ="./data/players.csv"
outputfile ="./data/y_topredict.csv"
generate_y_rows(playersfile, atpurl, "2023-08-24")