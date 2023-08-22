import pandas as pd
import numpy as np
import datetime
import math


def generate_training_dataset(atp_data_file, player_file, year_start, year_end, training_file): 
    # loading data in memory
    players = pd.read_csv(player_file)
    matches=pd.read_csv(atp_data_file)
    matches.Date = matches.Date.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))

    # filtering the data raw to the wanted years
    matches = matches.loc[(matches.Date.dt.year >= year_start) & (matches.Date.dt.year <= year_end)]


    player1_name=[]
    player1_ATPRank=[]
    player1_games=[]
    player1_wins=[]
    player1_loses=[]

    player2_name=[]
    player2_ATPRank=[]
    player2_games=[]
    player2_wins=[]
    player2_loses=[]

    match_date=[]
    match_location=[]
    match_tournament=[]
    match_surface=[]
    match_competition=[]
    match_odd_player1=[]
    match_odd_player2=[]

    winner_player1=[]

    for index, row in matches.iterrows():
        player1 = players.loc[players.name == row.Winner]
        player2 = players.loc[players.name == row.Loser]
        if player1.size!=0:
            player1_name.append(player1.iloc[0]["name"])
            player1_ATPRank.append(player1.iloc[0]["ATPRank"])
            player1_games.append(player1.iloc[0]["games"])
            player1_wins.append(player1.iloc[0]["wins"])
            player1_loses.append(player1.iloc[0]["loses"])
        else:
            player1_name.append(row.Winner)
            player1_ATPRank.append(math.nan)
            player1_games.append(math.nan)
            player1_wins.append(math.nan)
            player1_loses.append(math.nan)

        if player2.size!=0:
            player2_name.append(player2.iloc[0]["name"])
            player2_ATPRank.append(player2.iloc[0]["ATPRank"])
            player2_games.append(player2.iloc[0]["games"])
            player2_wins.append(player2.iloc[0]["wins"])
            player2_loses.append(player2.iloc[0]["loses"])
        else:
            player2_name.append(row.Loser)
            player2_ATPRank.append(math.nan)
            player2_games.append(math.nan)
            player2_wins.append(math.nan)
            player2_loses.append(math.nan)

        match_date.append(row.Date)
        match_surface.append(row.Surface)
        match_location.append(row.Location)
        match_tournament.append(row.Tournament)
        match_odd_player1.append(row.B365W)
        match_odd_player2.append(row.B365L)
        winner_player1.append(1)

    d = {
        'player1_name': player1_name, 
        'player1_atprank':player1_ATPRank,
        'player1_games':player1_games,
        'player1_wins':player1_wins,
        'player1_loses':player1_loses,

        'player2_name' : player2_name,
        'player2_atprank':player2_ATPRank,
        'player2_games':player2_games,
        'player2_wins':player2_wins,
        'player2_loses':player2_loses,

        'match_date': match_date,
        'match_location':match_location,
        'match_tournament':match_tournament,
        'match_surface': match_surface,
        'match_odd_player1':match_odd_player1,
        'match_odd_player2':match_odd_player2,
        'winner_player1' : winner_player1}

    training_matches = pd.DataFrame(data=d)
    training_matches.to_csv(training_file,index=False)