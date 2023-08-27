from match_stats_match_info import tourney_matches
from match_stats_tourney_list import tourneys
from match_stats_players_data_extended import match_data_extended
from match_stats_players_data import match_data
from scraping import add2csv,html2csv

from selenium import webdriver 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time 

def generate_match_stats(): 
    # User selects year
    matchs = pd.read_csv("./data/matchs.csv")

    #tourney_year_id,tourney_order,tourney_name,tourney_slug,
    #tourney_url_suffix,start_date,start_year,start_month,start_day,
    #end_date,end_year,end_month,end_day,currency,prize_money,match_index,
    #tourney_round_name,round_order,match_order,winner_name,winner_player_id,
    #winner_slug,loser_name,loser_player_id,loser_slug,winner_seed,loser_seed,
    #match_score_tiebreaks,winner_sets_won,loser_sets_won,winner_games_won,
    #loser_games_won,winner_tiebreaks_won,loser_tiebreaks_won,match_id,match_stats_url_suffix

    #tourney_url_suffix, tourney_name, tourney_
    url_prefix = 'https://www.atptour.com'
    csv_filename = "stats.csv"
    extended_csv_filename = "stats-extended.csv"

    for index, match in matchs.iterrows():
        match_stats_url = url_prefix + match.match_stats_url_suffix
        
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.page_load_strategy = 'normal' 
        chrome_path = "./bin/chromedriver.exe" #ChromeDriverManager()#.install() 
        chrome_service = Service(chrome_path) 
        driver = Chrome(options=options, service=chrome_service)
        driver.implicitly_wait(10) 

        driver.get(match_stats_url)
        try :
            driver.find_element(By.CLASS_NAME, "StatsHeader") ## this is a dummy to apply the implicit wait
        except:
            print("selenium loading exception:", match_stats_url)
        html = driver.page_source

        print(match_stats_url)
        html2csv(html,"./data/scrapping" + str(index) + ".txt")

        if html.find('Net points won') > 0:
            print("find netpoint")
            if match_data_extended(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
                print("gere")
                scraped_data = match_data_extended(html, match.winner_player_id, match.loser_player_id)
                csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
                csv_row_data_extended = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + [scraped_data[2]] + scraped_data[56:66] + [scraped_data[29]] + scraped_data[66:76]
                add2csv(csv_row_data, csv_filename)
                add2csv(csv_row_data_extended, extended_csv_filename)
        else:
            print("find NOT netpoint")
            if match_data(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
                print("qsdqsd")
                scraped_data = match_data(html, match.winner_player_id, match.loser_player_id)
                csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
                add2csv(csv_row_data, csv_filename)

        