import pandas as pd 
import numpy as np
from datetime import datetime

def generate_dataset(atptournamentfile, atpmatchfile, atpmatchstatsfile,playersfile,coukfile,outputfile):
    matchs = pd.read_csv(atpmatchfile)
    matchs_stats = pd.read_csv(atpmatchstatsfile)
    couk = pd.read_csv(coukfile)
    tournaments = pd.read_csv(atptournamentfile)
    players = pd.read_csv(playersfile)

    # Sometimes atp matchs scrapped do not have accurate tournament date, 
    # So we merge match en tournaments to take tournaments col we are more confident on
    # matchs.loc[matchs.start_year.isna()] # = 550
    # tournaments.loc[tournaments.year.isna()] # = 0
    # dropping tournaments info from matchs
    #matchs = matchs.drop(["tourney_order","tourney_name","tourney_slug","tourney_url_suffix","start_date","start_year","start_month","start_day","end_date","end_year","end_month", "end_day", "currency","prize_money","match_index"],axis=1)
    matchs = matchs[["match_id", "tourney_year_id","tourney_round_name","round_order","match_order","match_score_tiebreaks",
                    "winner_name","winner_player_id","winner_slug","winner_games_won","winner_sets_won","winner_tiebreaks_won",
                    "loser_name","loser_player_id","loser_slug","loser_games_won","loser_sets_won","loser_tiebreaks_won"]]

    tournaments = tournaments[["tourney_year_id","tourney_order","tourney_type","tourney_name",
                            "tourney_location","tourney_date","tourney_conditions","tourney_surface",
                            "currency","tourney_fin_commit"]]
    tournaments["tourney_currency"] = tournaments["currency"]
    tournaments = tournaments.drop(["currency"],axis=1)

    atpmatchs = pd.merge(matchs, tournaments, how="left", left_on ="tourney_year_id", right_on = "tourney_year_id")

    atpmatchs1player = pd.merge(atpmatchs, players, how="left", left_on ="winner_player_id", right_on = "player_id",  suffixes=('', '_winner'))
    atpmatchs2player = pd.merge(atpmatchs1player, players, how="left", left_on ="loser_player_id", right_on = "player_id", suffixes=('_winner', '_loser'))

    key=[]
    for index, row in atpmatchs2player.iterrows():
        key.append(str(datetime.strptime(row.tourney_date,'%Y.%m.%d').year) + str(datetime.strptime(row.tourney_date,'%Y.%m.%d').month) + row.last_name_winner.split(" ")[0] +  row.last_name_loser.split(" ")[0])
    atpmatchs2player["key"]=key

    key=[]
    couk = couk[["Date","Winner","Loser","WRank","LRank","B365W","B365L","PSW","PSL"]]
    for index, row in couk.iterrows():
        key.append(str(datetime.strptime(row.Date,'%Y-%m-%d').year) + str(datetime.strptime(row.Date,'%Y-%m-%d').month) + row.Winner.split(" ")[0] +  row.Loser.split(" ")[0])
    couk["key"]=key

    atpmatchs_odds = pd.merge(atpmatchs2player, couk, how="left", left_on ="key", right_on = "key")


    matchs_stats = matchs_stats[["match_id", "match_time","match_duration",
                                "winner_serve_rating","winner_aces","winner_double_faults","winner_first_serves_in",
                                "winner_first_serves_total","winner_first_serve_points_won","winner_first_serve_points_total",
                                "winner_second_serve_points_won","winner_second_serve_points_total","winner_break_points_saved","winner_break_points_serve_total",
                                "winner_service_games_played","winner_return_rating","winner_first_serve_return_won","winner_first_serve_return_total","winner_second_serve_return_won",
                                "winner_second_serve_return_total","winner_break_points_converted",
    "winner_break_points_return_total",
    "winner_return_games_played",
    "winner_service_points_won",	"winner_service_points_total",
    "winner_return_points_won",	"winner_return_points_total",
    "winner_total_points_won",	"winner_total_points_total",
    "loser_serve_rating",	"loser_aces",
    "loser_double_faults",	"loser_first_serves_in",
    "loser_first_serves_total",	"loser_first_serve_points_won",	"loser_first_serve_points_total",	"loser_second_serve_points_won",
    "loser_second_serve_points_total",	"loser_break_points_saved",	"loser_break_points_serve_total",	"loser_service_games_played",	
    "loser_return_rating",
    "loser_first_serve_return_won",	"loser_first_serve_return_total",	"loser_second_serve_return_won",	
    "loser_second_serve_return_total",	"loser_break_points_converted",
    "loser_break_points_return_total",	"loser_return_games_played",	"loser_service_points_won",
    "loser_service_points_total",	"loser_return_points_won",	"loser_return_points_total",
    "loser_total_points_won",	"loser_total_points_total"]]

    atpmatchs_stats_odds = pd.merge(atpmatchs_odds, matchs_stats, how="left", left_on ="match_id", right_on = "match_id")
    atpmatchs_stats_odds.to_csv(outputfile,index=False)




