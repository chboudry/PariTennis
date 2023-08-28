from scrap_atp_match_stats_players_data_extended import match_data_extended
from scrap_atp_match_stats_players_data import match_data
from scrap_atp_utils import *
import sys

from selenium import webdriver 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import random
import time
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
        #if index%10 == 0:
        #    print("ici")
        #    time.sleep(30)
        if str(match.start_date) == 'nan':
            generate_match_stats_b2018(match, matchsstats_file, matchstatsadvanced_file)
        elif (datetime.strptime(match.start_date, '%Y.%m.%d') < datetime.strptime(datetime_str,'%Y.%m.%d')):
            generate_match_stats_b2018(match, matchsstats_file, matchstatsadvanced_file)
        else:
            generate_match_stats_a2018(match, matchsstats_file, matchstatsadvanced_file)


def scrape_match_stats(match):
    url_prefix = 'https://www.atptour.com'
    url_match = url_prefix + match.match_stats_url_suffix
    match_tree = html_parse_tree(url_match)
    # Match time
    try:
        match_time_xpath = "//td[contains(@class, 'time')]/text()"
        match_time_parsed = xpath_parse(match_tree, match_time_xpath)
        match_time_cleaned = regex_strip_array(match_time_parsed)
        match_time = match_time_cleaned[0].replace("Time: ", "")
        match_time_split = match_time.split(":")            
        match_time_hours = int(match_time_split[0])
        match_time_minutes = int(match_time_split[1])
        match_duration = 60*match_time_hours + match_time_minutes                                        
    except Exception:
        match_time = ""
        match_duration = ""

    # Match info

    match_year = match.match_stats_url_suffix.split('/')[3]

    # This is for pre-2020
    #tourney_id = match_stats_url_suffix.split('/')[4]
    #match_index = match_stats_url_suffix.split('/')[5]

    # This is for 2020 through most of 2021
    tourney_id = match.match_stats_url_suffix.split('/')[6]
    match_index = match.match_stats_url_suffix.split('/')[7]

    try:
        winner_slug_xpath = "//div[@class='player-left-name']/a/@href"
        winner_slug_parsed = xpath_parse(match_tree, winner_slug_xpath)
        winner_slug = winner_slug_parsed[0].split('/')[4]
    except Exception:
        winner_slug = ''

    try:
        loser_slug_xpath = "//div[@class='player-right-name']/a/@href"
        loser_slug_parsed = xpath_parse(match_tree, loser_slug_xpath)
        loser_slug = loser_slug_parsed[0].split('/')[4]
    except Exception:
        loser_slug = ''

    match_id = match.match_id

    # # # # # # # #
    # Match stats #
    # # # # # # # #
    
    try:                
        # Stats Xpaths
        left_stats_xpath = "//td[@class='match-stats-number-left']/span/text()"
        left_stats_parsed = xpath_parse(match_tree, left_stats_xpath)
        left_stats_cleaned = regex_strip_array(left_stats_parsed)

        right_stats_xpath = "//td[@class='match-stats-number-right']/span/text()"
        right_stats_parsed = xpath_parse(match_tree, right_stats_xpath)
        right_stats_cleaned = regex_strip_array(right_stats_parsed)        

        # Ratings Xpaths
        left_ratings_xpath = "//td[@class='match-stats-number-left']/span/a/text()"
        left_ratings_parsed = xpath_parse(match_tree, left_ratings_xpath)
        right_ratings_xpath = "//td[@class='match-stats-number-right']/span/a/text()"
        right_ratings_parsed = xpath_parse(match_tree, right_ratings_xpath)

        # Left stats
        left_serve_rating = int(left_ratings_parsed[0])
        left_aces = int(left_stats_cleaned[2])
        left_double_faults = int(left_stats_cleaned[3])

        left_first_serves_in = int(fraction_stats(left_stats_cleaned[5])[0])
        left_first_serves_total = int(fraction_stats(left_stats_cleaned[5])[1])

        left_first_serve_points_won = int(fraction_stats(left_stats_cleaned[7])[0])
        left_first_serve_points_total = int(fraction_stats(left_stats_cleaned[7])[1])

        left_second_serve_points_won = int(fraction_stats(left_stats_cleaned[9])[0])
        left_second_serve_points_total = int(fraction_stats(left_stats_cleaned[9])[1])

        left_break_points_saved = int(fraction_stats(left_stats_cleaned[11])[0])
        left_break_points_serve_total = int(fraction_stats(left_stats_cleaned[11])[1])

        left_service_points_won = int(fraction_stats(left_stats_cleaned[23])[0])
        left_service_points_total = int(fraction_stats(left_stats_cleaned[23])[1])

        left_return_rating = int(left_ratings_parsed[1])
        left_first_serve_return_won = int(fraction_stats(left_stats_cleaned[16])[0])
        left_first_serve_return_total = int(fraction_stats(left_stats_cleaned[16])[1])

        left_second_serve_return_won = int(fraction_stats(left_stats_cleaned[18])[0])
        left_second_serve_return_total = int(fraction_stats(left_stats_cleaned[18])[1])

        left_break_points_converted = int(fraction_stats(left_stats_cleaned[20])[0])
        left_break_points_return_total = int(fraction_stats(left_stats_cleaned[20])[1])

        left_service_games_played = int(left_stats_cleaned[12])
        left_return_games_played = int(left_stats_cleaned[21])

        left_return_points_won = int(fraction_stats(left_stats_cleaned[25])[0])
        left_return_points_total = int(fraction_stats(left_stats_cleaned[25])[1])

        left_total_points_won = int(fraction_stats(left_stats_cleaned[27])[0])
        left_total_points_total = int(fraction_stats(left_stats_cleaned[27])[1])
        
        # Loser stats
        right_serve_rating = int(right_ratings_parsed[0])
        right_aces = int(right_stats_cleaned[2])
        right_double_faults = int(right_stats_cleaned[3])

        right_first_serves_in = int(fraction_stats(right_stats_cleaned[5])[0])
        right_first_serves_total = int(fraction_stats(right_stats_cleaned[5])[1])

        right_first_serve_points_won = int(fraction_stats(right_stats_cleaned[7])[0])
        right_first_serve_points_total = int(fraction_stats(right_stats_cleaned[7])[1])

        right_second_serve_points_won = int(fraction_stats(right_stats_cleaned[9])[0])
        right_second_serve_points_total = int(fraction_stats(right_stats_cleaned[9])[1])

        right_break_points_saved = int(fraction_stats(right_stats_cleaned[11])[0])
        right_break_points_serve_total = int(fraction_stats(right_stats_cleaned[11])[1])

        right_service_points_won = int(fraction_stats(right_stats_cleaned[23])[0])
        right_service_points_total = int(fraction_stats(right_stats_cleaned[23])[1])

        right_return_rating = int(right_ratings_parsed[1])
        right_first_serve_return_won = int(fraction_stats(right_stats_cleaned[16])[0])
        right_first_serve_return_total = int(fraction_stats(right_stats_cleaned[16])[1])

        right_second_serve_return_won = int(fraction_stats(right_stats_cleaned[18])[0])
        right_second_serve_return_total = int(fraction_stats(right_stats_cleaned[18])[1])

        right_break_points_converted = int(fraction_stats(right_stats_cleaned[20])[0])
        right_break_points_return_total = int(fraction_stats(right_stats_cleaned[20])[1])

        right_service_games_played = int(right_stats_cleaned[12])
        right_return_games_played = int(right_stats_cleaned[21])

        right_return_points_won = int(fraction_stats(right_stats_cleaned[25])[0])
        right_return_points_total = int(fraction_stats(right_stats_cleaned[25])[1])

        right_total_points_won = int(fraction_stats(right_stats_cleaned[27])[0])
        right_total_points_total = int(fraction_stats(right_stats_cleaned[27])[1])

        # # # # # # # # # # # # # # # # # # #
        # Assign stats to winner and loser  #
        # # # # # # # # # # # # # # # # # # #

        # Left player url
        left_player_url_xpath = "//div[@class='player-left-name']/a/@href"
        left_player_url_xpath_parsed = xpath_parse(match_tree, left_player_url_xpath)
            
        # Right player url
        right_player_url_xpath = "//div[@class='player-right-name']/a/@href"
        right_player_url_xpath_parsed = xpath_parse(match_tree, right_player_url_xpath)                

        if left_player_url_xpath_parsed == winner_slug_parsed:
            winner_serve_rating = left_serve_rating
            winner_aces = left_aces
            winner_double_faults = left_double_faults
            winner_first_serves_in = left_first_serves_in
            winner_first_serves_total = left_first_serves_total
            winner_first_serve_points_won = left_first_serve_points_won
            winner_first_serve_points_total = left_first_serve_points_total
            winner_second_serve_points_won = left_second_serve_points_won
            winner_second_serve_points_total = left_second_serve_points_total
            winner_break_points_saved = left_break_points_saved
            winner_break_points_serve_total = left_break_points_serve_total
            winner_service_points_won = left_service_points_won
            winner_service_points_total = left_service_points_total
            winner_return_rating = left_return_rating
            winner_first_serve_return_won = left_first_serve_return_won
            winner_first_serve_return_total = left_first_serve_return_total
            winner_second_serve_return_won = left_second_serve_return_won
            winner_second_serve_return_total = left_second_serve_return_total
            winner_break_points_converted = left_break_points_converted
            winner_break_points_return_total = left_break_points_return_total
            winner_service_games_played = left_service_games_played
            winner_return_games_played = left_return_games_played
            winner_return_points_won = left_return_points_won
            winner_return_points_total = left_return_points_total
            winner_total_points_won = left_total_points_won
            winner_total_points_total = left_total_points_total

            loser_serve_rating = right_serve_rating
            loser_aces = right_aces
            loser_double_faults = right_double_faults
            loser_first_serves_in = right_first_serves_in
            loser_first_serves_total = right_first_serves_total
            loser_first_serve_points_won = right_first_serve_points_won
            loser_first_serve_points_total = right_first_serve_points_total
            loser_second_serve_points_won = right_second_serve_points_won
            loser_second_serve_points_total = right_second_serve_points_total
            loser_break_points_saved = right_break_points_saved
            loser_break_points_serve_total = right_break_points_serve_total
            loser_service_points_won = right_service_points_won
            loser_service_points_total = right_service_points_total
            loser_return_rating = right_return_rating
            loser_first_serve_return_won = right_first_serve_return_won
            loser_first_serve_return_total = right_first_serve_return_total
            loser_second_serve_return_won = right_second_serve_return_won
            loser_second_serve_return_total = right_second_serve_return_total
            loser_break_points_converted = right_break_points_converted
            loser_break_points_return_total = right_break_points_return_total
            loser_service_games_played = right_service_games_played
            loser_return_games_played = right_return_games_played
            loser_return_points_won = right_return_points_won
            loser_return_points_total = right_return_points_total
            loser_total_points_won = right_total_points_won
            loser_total_points_total = right_total_points_total                    

        elif right_player_url_xpath_parsed == winner_slug_parsed:
            winner_serve_rating = right_serve_rating
            winner_aces = right_aces
            winner_double_faults = right_double_faults
            winner_first_serves_in = right_first_serves_in
            winner_first_serves_total = right_first_serves_total
            winner_first_serve_points_won = right_first_serve_points_won
            winner_first_serve_points_total = right_first_serve_points_total
            winner_second_serve_points_won = right_second_serve_points_won
            winner_second_serve_points_total = right_second_serve_points_total
            winner_break_points_saved = right_break_points_saved
            winner_break_points_serve_total = right_break_points_serve_total
            winner_service_points_won = right_service_points_won
            winner_service_points_total = right_service_points_total
            winner_return_rating = right_return_rating
            winner_first_serve_return_won = right_first_serve_return_won
            winner_first_serve_return_total = right_first_serve_return_total
            winner_second_serve_return_won = right_second_serve_return_won
            winner_second_serve_return_total = right_second_serve_return_total
            winner_break_points_converted = right_break_points_converted
            winner_break_points_return_total = right_break_points_return_total
            winner_service_games_played = right_service_games_played
            winner_return_games_played = right_return_games_played
            winner_return_points_won = right_return_points_won
            winner_return_points_total = right_return_points_total
            winner_total_points_won = right_total_points_won
            winner_total_points_total = right_total_points_total

            loser_serve_rating = left_serve_rating
            loser_aces = left_aces
            loser_double_faults = left_double_faults
            loser_first_serves_in = left_first_serves_in
            loser_first_serves_total = left_first_serves_total
            loser_first_serve_points_won = left_first_serve_points_won
            loser_first_serve_points_total = left_first_serve_points_total
            loser_second_serve_points_won = left_second_serve_points_won
            loser_second_serve_points_total = left_second_serve_points_total
            loser_break_points_saved = left_break_points_saved
            loser_break_points_serve_total = left_break_points_serve_total
            loser_service_points_won = left_service_points_won
            loser_service_points_total = left_service_points_total
            loser_return_rating = left_return_rating
            loser_first_serve_return_won = left_first_serve_return_won
            loser_first_serve_return_total = left_first_serve_return_total
            loser_second_serve_return_won = left_second_serve_return_won
            loser_second_serve_return_total = left_second_serve_return_total
            loser_break_points_converted = left_break_points_converted
            loser_break_points_return_total = left_break_points_return_total
            loser_service_games_played = left_service_games_played
            loser_return_games_played = left_return_games_played
            loser_return_points_won = left_return_points_won
            loser_return_points_total = left_return_points_total
            loser_total_points_won = left_total_points_won
            loser_total_points_total = left_total_points_total                          
    except Exception:
        winner_serve_rating = ''
        winner_aces = ''
        winner_double_faults = ''
        winner_first_serves_in = ''
        winner_first_serves_total = ''
        winner_first_serve_points_won = ''
        winner_first_serve_points_total = ''
        winner_second_serve_points_won = ''
        winner_second_serve_points_total = ''
        winner_break_points_saved = ''
        winner_break_points_serve_total = ''
        winner_service_points_won = ''
        winner_service_points_total = ''
        winner_return_rating = ''
        winner_first_serve_return_won = ''
        winner_first_serve_return_total = ''
        winner_second_serve_return_won = ''
        winner_second_serve_return_total = ''
        winner_break_points_converted = ''
        winner_break_points_return_total = ''
        winner_service_games_played = ''
        winner_return_games_played = ''
        winner_return_points_won = ''
        winner_return_points_total = ''
        winner_total_points_won = ''
        winner_total_points_total = ''

        loser_serve_rating = ''
        loser_aces = ''
        loser_double_faults = ''
        loser_first_serves_in = ''
        loser_first_serves_total = ''
        loser_first_serve_points_won = ''
        loser_first_serve_points_total = ''
        loser_second_serve_points_won = ''
        loser_second_serve_points_total = ''
        loser_break_points_saved = ''
        loser_break_points_serve_total = ''
        loser_service_points_won = ''
        loser_service_points_total = ''
        loser_return_rating = ''
        loser_first_serve_return_won = ''
        loser_first_serve_return_total = ''
        loser_second_serve_return_won = ''
        loser_second_serve_return_total = ''
        loser_break_points_converted = ''
        loser_break_points_return_total = ''
        loser_service_games_played = ''
        loser_return_games_played = ''
        loser_return_points_won = ''
        loser_return_points_total = ''
        loser_total_points_won = ''
        loser_total_points_total = ''                    

    # Store data
    output = [match_id, match.tourney_slug, match.match_stats_url_suffix, match_time, match_duration, match.winner_player_id, winner_serve_rating, winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_points_won, winner_first_serve_points_total, winner_second_serve_points_won, winner_second_serve_points_total, winner_break_points_saved, winner_break_points_serve_total, winner_service_games_played, winner_return_rating, winner_first_serve_return_won, winner_first_serve_return_total, winner_second_serve_return_won, winner_second_serve_return_total, winner_break_points_converted, winner_break_points_return_total, winner_return_games_played, winner_service_points_won, winner_service_points_total, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total, match.loser_player_id, loser_serve_rating, loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_points_won, loser_first_serve_points_total, loser_second_serve_points_won, loser_second_serve_points_total, loser_break_points_saved, loser_break_points_serve_total, loser_service_games_played, loser_return_rating, loser_first_serve_return_won, loser_first_serve_return_total, loser_second_serve_return_won, loser_second_serve_return_total, loser_break_points_converted, loser_break_points_return_total, loser_return_games_played, loser_service_points_won, loser_service_points_total, loser_return_points_won, loser_return_points_total, loser_total_points_won, loser_total_points_total]
    return output
    

def generate_match_stats_b2018(match, matchsstats_file, matchstatsadvanced_file): 
    scraped_stats = scrape_match_stats(match)
    add2csv(scraped_stats, matchsstats_file)

def generate_match_stats_a2018(match, matchsstats_file, matchstatsadvanced_file): 
    url_prefix = 'https://www.atptour.com'

    if match.match_score_tiebreaks != "(W/O)":
        while True:
            try:
                match_stats_url = url_prefix + match.match_stats_url_suffix

                options = ChromeOptions()
                options.add_argument("--headless=new")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.page_load_strategy = 'normal' 
                chrome_path = "./bin/chromedriver.exe" #ChromeDriverManager()#.install() 
                chrome_service = Service(chrome_path) 
                driver = Chrome(options=options, service=chrome_service)
                
                driver.get(match_stats_url)

                WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME, "StatsHeader")))## this is a dummy to apply the implicit wait
                html = driver.page_source

                if html.find('Net points won') > 0:
                    if match_data_extended(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
                        scraped_data = match_data_extended(html, match.winner_player_id, match.loser_player_id)
                        csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
                        csv_row_data_extended = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + [scraped_data[2]] + scraped_data[56:66] + [scraped_data[29]] + scraped_data[66:76]
                        print(csv_row_data)
                        add2csv(csv_row_data, matchsstats_file)
                        add2csv(csv_row_data_extended, matchstatsadvanced_file)
                else:
                    if match_data(html, match.winner_player_id, match.loser_player_id) != 'MISSING DATA':
                        scraped_data = match_data(html, match.winner_player_id, match.loser_player_id)
                        csv_row_data = [match.match_id, match.tourney_slug, match.match_stats_url_suffix] + scraped_data[0:56]
                        print(csv_row_data)
                        add2csv(csv_row_data, matchsstats_file)

                driver.quit()
            except :
                html = driver.page_source
                print(match_stats_url)
                html2csv(html,"./data/scrapping" + str(random.randint(0,100)) + ".txt")
                driver.stop_client()
                driver.close()
                driver.quit()
                time.sleep(60)
                continue
            break

    