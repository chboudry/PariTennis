from scrap_atp_utils import *
import pandas as pd


def generate_players(matchsfile, outputfile):
    player_url_suffixes = player_url_suffixes_array(matchsfile)
    generate_players_sub(player_url_suffixes, outputfile)

def generate_players_sub(player_url_suffixes, outputfile):
    url_prefix = 'https://www.atptour.com'

    data = ["player_id", "first_name", "last_name", "country_code", "birthdate", "birth_year", "birth_month", "birth_day", "turned_pro", "weight_kg", "weight_lbs", "height_cm", "height_in", "birthplace"]
    add2csv(data, outputfile)

    for player_url_suffix in player_url_suffixes:
        player_url = url_prefix + player_url_suffix
        print(player_url)
        player_id = player_url.split('/')[6]
        player_tree = html_parse_tree(player_url)
        try:
            first_name = regex_strip_array(xpath_parse(player_tree, '//*[@id="playerProfileHero"]/div[2]/div[1]/div/div[1]/div[1]/text()'))[0]
            last_name = regex_strip_array(xpath_parse(player_tree, '//*[@id="playerProfileHero"]/div[2]/div[1]/div/div[1]/div[2]/text()'))[0]
        except:
            data = [player_id, '', '', '', '', '', '', '', '', '', '', '', '', '']
            add2csv(data, outputfile)
            continue

        try:
            country_code = regex_strip_array(xpath_parse(player_tree, '//*[@id="playerProfileHero"]/div[2]/div[1]/div/div[3]/div[2]/div[2]/text()'))[0]
        except Exception:
            country_code = ''
        try: 
            birthdate = regex_strip_array(xpath_parse(player_tree, '//span[@class="table-birthday"]/text()'))[0].replace('(','').replace(')','')
            birth_year = birthdate.split('.')[0]
            if birthdate.split('.')[1][0] == '0': birth_month = birthdate.split('.')[1][1]
            else: birth_month = birthdate.split('.')[1]
            if birthdate.split('.')[2][0] == '0': birth_day = birthdate.split('.')[2][1]
            else: birth_day = birthdate.split('.')[2]
        except Exception:
            birthdate = ''
            birth_year = ''
            birth_month = ''
            birth_day = ''

        turned_pro = regex_strip_array(xpath_parse(player_tree, '//div[@class="table-big-value"]/text()'))[2]

        try:
            weight_kg = regex_strip_array(xpath_parse(player_tree, '//span[@class="table-weight-kg-wrapper"]/text()'))[0].replace('kg','').replace('(','').replace(')','')
            weight_lbs = regex_strip_array(xpath_parse(player_tree, '//span[@class="table-weight-lbs"]/text()'))[0]
        except Exception:
            weight_kg = ''
            weight_lbs = ''
        
        try:
            height_cm = regex_strip_array(xpath_parse(player_tree, '//span[@class="table-height-cm-wrapper"]/text()'))[0].replace('cm','').replace('(','').replace(')','')
            height_ft = regex_strip_array(xpath_parse(player_tree, '//span[@class="table-height-ft"]/text()'))[0]
            height_ft_split = height_ft.split("'")
            height_in = 12 * int(height_ft_split[0]) + int(height_ft_split[1].replace('"',''))
        except Exception:
            height_cm = ''
            height_in = ''

        birthplace = regex_strip_array(xpath_parse(player_tree, '//div[@class="table-value"]/text()'))[0]

        try:
            plays = regex_strip_array(xpath_parse(player_tree, '//div[@class="table-value"]/text()'))[1].split(',')
            handedness = plays[0]
            backhand = plays[1].lstrip()
        except Exception:
            handedness = ''
            backhand = ''

        data = [player_id, first_name, last_name, country_code, birthdate, birth_year, birth_month, birth_day, turned_pro, weight_kg, weight_lbs, height_cm, height_in, birthplace]
        
        add2csv(data, outputfile)

def player_url_suffixes_array(matchsfile):
    matchs = pd.read_csv(matchsfile)
    #"/en/players/jimmy-connors/c044/overview",
    players_url=[]
    for row_id, match in matchs.iterrows():
        players_url.append("/en/players/" + match.winner_slug + "/" + match.winner_player_id + "/overview")
        players_url.append("/en/players/" + match.loser_slug + "/" + match.loser_player_id + "/overview")

    players_url = set(players_url)
    add2csv(players_url, "./data/players_suffix.csv")
    return players_url

def update_rankings(playersfile):
    #https://www.atptour.com/en/rankings/singles?rankDate=2023-8-28&countryCode=all&rankRange=0-2000