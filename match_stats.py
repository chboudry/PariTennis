from match_stats_players_data_extended import match_data_extended
from match_stats_players_data import match_data
from scraping import add2csv,html2csv

from selenium import webdriver 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
from datetime import datetime

def generate_match_stats(matchs_file, matchsstats_file, matchstatsadvanced_file): 
    matchs = pd.read_csv(matchs_file)

    col_match_data = ["match_id", "tourney_slug", "match_stats_url_suffix", "match_time", "match_duration"]
    col_winner_data = ["winner_player_id", "winner_serve_rating", "winner_aces", "winner_double_faults", "winner_first_serves_in", "winner_first_serves_total", "winner_first_serve_points_won", "winner_first_serve_points_total", "winner_second_serve_points_won", "winner_second_serve_points_total", "winner_break_points_saved", "winner_break_points_serve_total", "winner_service_games_played", "winner_return_rating", "winner_first_serve_return_won", "winner_first_serve_return_total", "winner_second_serve_return_won", "winner_second_serve_return_total", "winner_break_points_converted", "winner_break_points_return_total", "winner_return_games_played", "winner_service_points_won", "winner_service_points_total", "winner_return_points_won", "winner_return_points_total", "winner_total_points_won", "winner_total_points_total"]
    col_loser_data = ["loser_player_id", "loser_serve_rating", "loser_aces", "loser_double_faults", "loser_first_serves_in", "loser_first_serves_total", "loser_first_serve_points_won", "loser_first_serve_points_total", "loser_second_serve_points_won", "loser_second_serve_points_total", "loser_break_points_saved", "loser_break_points_serve_total", "loser_service_games_played", "loser_return_rating", "loser_first_serve_return_won", "loser_first_serve_return_total", "loser_second_serve_return_won", "loser_second_serve_return_total", "loser_break_points_converted", "loser_break_points_return_total", "loser_return_games_played", "loser_service_points_won", "loser_service_points_total", "loser_return_points_won", "loser_return_points_total", "loser_total_points_won", "loser_total_points_total"]
    cols = col_match_data + col_winner_data + col_loser_data
    add2csv(cols, matchsstats_file)

    col_winner_data_extended = ["winner_net_points_won", "winner_net_points_total", "winner_winners", "winner_unforced_errors", "winner_max_service_speed_kmh", "winner_max_service_speed_mph", "winner_avg_1st_serve_speed_kmh", "winner_avg_1st_serve_speed_mph", "winner_avg_2nd_serve_speed_kmh", "winner_avg_2nd_serve_speed_mph"]
    col_loser_data_extended = ["loser_net_points_won", "loser_net_points_total", "loser_winners", "loser_unforced_errors", "loser_max_service_speed_kmh", "loser_max_service_speed_mph", "loser_avg_1st_serve_speed_kmh", "loser_avg_1st_serve_speed_mph", "loser_avg_2nd_serve_speed_kmh", "loser_avg_2nd_serve_speed_mph"]
    cols_extended = col_match_data + ["winner_player_id"] + col_winner_data_extended + ["loser_player_id"] + col_loser_data_extended
    add2csv(cols_extended, matchstatsadvanced_file)

    datetime_str = '2021.10.18'

    for index, match in matchs.iterrows():
        if str(match.start_date) == 'nan':
            print("null")
        elif (datetime.strptime(match.start_date, '%Y.%m.%d') < datetime.strptime(datetime_str,'%Y.%m.%d')):
            print("torototo")
        else:
            generate_match_stats_a2018(match, matchsstats_file, matchstatsadvanced_file)



def generate_match_stats_b2018(match, matchsstats_file, matchstatsadvanced_file): 
    return

def generate_match_stats_a2018(match, matchsstats_file, matchstatsadvanced_file): 
    #tourney_url_suffix, tourney_name, tourney_
    url_prefix = 'https://www.atptour.com'

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
    #html2csv(html,"./data/scrapping" + str(index) + ".txt")

    if html.find('Net points won') > 0:
        if match_data_extended(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
            scraped_data = match_data_extended(html, match.winner_player_id, match.loser_player_id)
            csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
            csv_row_data_extended = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + [scraped_data[2]] + scraped_data[56:66] + [scraped_data[29]] + scraped_data[66:76]
            add2csv(csv_row_data, matchsstats_file)
            add2csv(csv_row_data_extended, matchstatsadvanced_file)
    else:
        if match_data(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
            scraped_data = match_data(html, match.winner_player_id, match.loser_player_id)
            csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
            add2csv(csv_row_data, matchsstats_file)

    