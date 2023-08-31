import pandas as pd 
import numpy as np
from datetime import datetime
from shuffle_training_dataset import *

df = pd.read_csv("./data_formatted/dataset.csv")

# Static features
#match_id,tourney_year_id,tourney_round_name,round_order,match_order,match_score_tiebreaks,
#winner_name,winner_player_id,
#winner_slug,winner_games_won,winner_sets_won,
#loser_name,loser_player_id,
#winner_tiebreaks_won,loser_slug,loser_games_won,loser_sets_won,
# loser_tiebreaks_won,tourney_order,tourney_type,tourney_name,tourney_location,
#tourney_date,tourney_conditions,tourney_surface,tourney_fin_commit,tourney_currency,
# player_id_winner,first_name_winner,last_name_winner,country_code_winner,birthdate_winner,
#birth_year_winner,birth_month_winner,birth_day_winner,turned_pro_winner,weight_kg_winner
# ,weight_lbs_winner,height_cm_winner,height_in_winner,birthplace_winner,player_id_loser,first_name_loser,
#last_name_loser,country_code_loser,birthdate_loser,birth_year_loser,birth_month_loser,birth_day_loser,
# turned_pro_loser,weight_kg_loser,weight_lbs_loser,height_cm_loser,height_in_loser,birthplace_loser
#,key,Date,Winner,Loser,WRank,LRank,B365W,B365L,PSW,PSL,match_time,
# match_duration,winner_serve_rating,winner_aces,winner_double_faults,winner_first_serves_in,
# winner_first_serves_total,winner_first_serve_points_won,
#winner_first_serve_points_total,winner_second_serve_points_won,winner_second_serve_points_total,
# winner_break_points_saved,winner_break_points_serve_total,winner_service_games_played,winner_return_rating
#,winner_first_serve_return_won,winner_first_serve_return_total,winner_second_serve_return_won,
# winner_second_serve_return_total,winner_break_points_converted,winner_break_points_return_total,
#winner_return_games_played,winner_service_points_won,winner_service_points_total,winner_return_points_won,
# winner_return_points_total,winner_total_points_won,winner_total_points_total,loser_serve_rating,
#loser_aces,loser_double_faults,loser_first_serves_in,loser_first_serves_total
# ,loser_first_serve_points_won,loser_first_serve_points_total,loser_second_serve_points_won,
# loser_second_serve_points_total,
#loser_break_points_saved,loser_break_points_serve_total,loser_service_games_played,
# loser_return_rating,loser_first_serve_return_won,loser_first_serve_return_total,loser_second_serve_return_won,
#loser_second_serve_return_total,loser_break_points_converted,loser_break_points_return_total,
#loser_return_games_played,loser_service_points_won,loser_service_points_total,loser_return_points_won,
# loser_return_points_total,loser_total_points_won,loser_total_points_total


# filter
df = df[["match_id","Date","round_order","match_order",
         "winner_name","weight_kg_winner","height_cm_winner","birthdate_winner","winner_serve_rating", "WRank","B365W","PSW",
         "loser_name","weight_kg_loser","height_cm_loser", "birthdate_loser", "loser_serve_rating","LRank","B365L","PSL"]]

# rename
df= df.rename(columns={
    "match_id": "match_id",
    "Date":"match_date",
    "round_order":"match_round_order",
    "match_order":"match_order",

    "winner_name":"player1_name",
    "weight_kg_winner":"player1_weight",
    "height_cm_winner":"player1_height",
    "birthdate_winner":"player1_birthdate",
    "winner_serve_rating":"player1_serve_rating",
    "WRank":"player1_atprank",
    "B365W":"player1_oddsB365",
    "PSW":"player1_oddsPS",
    

    "loser_name":"player2_name",
    "weight_kg_loser":"player2_weight",
    "height_cm_loser":"player2_height",
    "birthdate_loser":"player2_birthdate",
    "loser_serve_rating":"player2_serve_rating", 
    "LRank":"player2_atprank",
    "B365L":"player2_oddsB365",
    "PSL":"player2_oddsPS"})

df["winner_player1"] = 1

# cleanup
df= df.dropna(subset="match_date")

# Order
df.match_date = df.match_date.apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))
df = df.sort_values(["match_date","match_round_order"],ascending=[True,False])
df = df.reset_index()

df['player1_birthdate'] = pd.to_datetime(df['player1_birthdate'], format='%Y.%m.%d') 
df['player2_birthdate'] = pd.to_datetime(df['player2_birthdate'], format='%Y.%m.%d') 

end = df.shape[0]

player1_plays =[]
player1_wins =[]
player1_losses =[]
player1_age=[]
player1_mean_serve_rating=[]

player2_plays =[]
player2_wins =[]
player2_losses =[]
player2_age=[]
player2_mean_serve_rating=[]

# generate features derived from the past for each player
for index,row in df.iterrows():
    if index%500==0:
        print(str(index)+"/"+str(end)+" matches treated.")

    pastdf = df[0:index]

    # player1
    previous_matchs = pastdf.loc[(pastdf.player1_name == row.player1_name) | (pastdf.player2_name == row.player1_name)]
    player1_plays.append(len(previous_matchs))
    wins = previous_matchs.loc[pastdf.player1_name == row.player1_name]
    player1_wins.append(len(wins))
    losses = previous_matchs.loc[pastdf.player2_name == row.player1_name]
    player1_losses.append(len(losses))
    player1_age.append(str((row.match_date - row.player1_birthdate).days/ 365.25))
    player1_mean_serve_rating.append((wins[["player1_serve_rating"]].mean() + losses[["player2_serve_rating"]].mean())/2)
    
    # player2
    previous_matchs = pastdf.loc[(pastdf.player1_name == row.player2_name) | (pastdf.player2_name == row.player2_name)]
    player2_plays.append(len(previous_matchs))
    wins = previous_matchs.loc[pastdf.player1_name == row.player2_name]
    player2_wins.append(len(wins))
    loss = previous_matchs.loc[pastdf.player2_name == row.player2_name]
    player2_losses.append(len(loss))
    player2_age.append(str((row.match_date - row.player2_birthdate).days/ 365.25))
    player2_mean_serve_rating.append((wins[["player1_serve_rating"]].mean().values[0] + losses[["player2_serve_rating"]].mean().values[0])/2)

df["player1_plays"] = player1_plays 
df["player1_wins"] = player1_wins
df["player1_losses"] = player1_losses 
df["player1_age"] = player1_age
df["player1_mean_serve_rating"] = player1_mean_serve_rating

df["player2_plays"] =player2_plays
df["player2_wins"] = player2_wins
df["player2_losses"] = player2_losses
df["player2_age"] = player2_age
df["player2_mean_serve_rating"] = player2_mean_serve_rating

# we drop match result columns
df = df.drop(["player1_serve_rating","player2_serve_rating"],axis=1)

df.to_csv("./data_formatted/training_dataset.csv",index=False)

shuffle_training_dataset("./data_formatted/training_dataset.csv", "./data_formatted/training_dataset.csv")