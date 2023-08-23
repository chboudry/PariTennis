import pandas as pd
import numpy as np
import datetime
import math
from bs4 import BeautifulSoup as bs
import requests 


## atpurl = https://www.atptour.com/en/scores/current/us-open/560/daily-schedule
## date expected format is YYYY-MM-DD
def generate_y_from_date(atpurl, date): 
    page = requests.get(atpurl)  
    bs_atp = bs(page.content, "lxml")
    bs_atp.prettify().splitlines()[0:30]

    # get 
    y = []
    return y