import pandas as pd
import numpy as np
import datetime


def generate_player_global_file(atp_data_file, year_start, year_end, player_file):
    # loading data in memory
    data=pd.read_csv(atp_data_file)
    data.Date = data.Date.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))

    # filtering the data raw to the wanted years
    data = data.loc[(data.Date.dt.year >= year_start) & (data.Date.dt.year <= year_end)]

    # building player dataset
    losers = data['Loser'].unique()
    winners = data['Winner'].unique()
    players = np.concatenate([losers,winners])
    players = np.unique(players)

    players_atprank = []
    players_total_play = []
    players_wins = []
    players_loses = []
    players_odds = []
    indoors_win = []
    indoors_loss= []
    outdoors_win = []
    outdoors_loss= []

    for player in players : 
        ## last known atp rank
        last_match_played = data.loc[(data.Winner == player) | (data.Loser == player)].iloc[-1]
        if last_match_played.Winner == player:
            players_atprank.append(last_match_played.WRank)
        else:
            players_atprank.append(last_match_played.LRank)


        players_total_play.append(len(data.loc[data['Winner']==player]) + len(data.loc[data['Loser']==player]))
        players_wins.append(len(data.loc[data['Winner']==player]))
        players_loses.append(len(data.loc[data['Loser']==player]))
        players_odds.append((data.loc[data['Winner']==player].B365W.mean() + data.loc[data['Loser']==player].B365L.mean())/2)

        winner_values = data.loc[data['Winner']==player]["Court"].value_counts()
        if hasattr(winner_values, 'Indoor'):
            indoors_win.append(winner_values.Indoor)
        else: 
            indoors_win.append(0)

        if hasattr(winner_values, 'Outdoor'):
            outdoors_win.append(winner_values.Outdoor)
        else:
            outdoors_win.append(0)

        loser_values = data.loc[data['Loser']==player]["Court"].value_counts()
        if hasattr(loser_values, 'Indoor'):
            indoors_loss.append(loser_values.Indoor)
        else:
            indoors_loss.append(0)
            
        if hasattr(loser_values, 'Outdoor'):
            outdoors_loss.append(loser_values.Outdoor)
        else:
            outdoors_loss.append(0)

    d = {
        'name': players, 
        'ATPRank':players_atprank,
        'games': players_total_play, 
        'wins':players_wins, 
        'loses':players_loses,
        'players_odds':players_odds,
        'indoors_win': indoors_win,
        'indoors_loss': indoors_loss,
        'outdoors_win': outdoors_win,
        'outdoors_loss': outdoors_loss}
    
    df_players = pd.DataFrame(data=d)
    df_players["ratio_win"] = df_players["wins"]/df_players["games"]
    df_players["players_indoors_win_ratio"] = df_players.indoors_win / (df_players.indoors_win + df_players.indoors_loss)
    df_players["players_outdoors_win_ratio"] = df_players.outdoors_win / (df_players.outdoors_win + df_players.outdoors_loss)
    df_players.to_csv(player_file,index=False)
