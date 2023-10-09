import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import config
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import seaborn as sns

title = "Jeu de données et webscrapping"
sidebar_name = "Jeu de données et webscraping"


def run():
    df = pd.read_csv(config.CO_UK_DATA_PATH, low_memory=False)
    st.title(title)

    st.markdown(
        """
        ## Exploration des données
        Pour ce projet, nous disposons de 2 bases de données (ATP, Confidence). 
        La base ATP comporte 57420 matchs décrits selon 22 variables d'études :
        -	6 portent sur les tournois dont 1 variables quantitatives et 5 variables catégorielles (ATP, Location, Tournament, Séries, Court, Surface)
        -	9 portent sur les joueurs dont 3 variables quantitatives et 6 variables catégorielles (Round, Best of, Winner, Loser, WRank, LRank, Wsets, Lsets, Comment)
        -	4 portent sur les bookmakers, toutes quantitatives : PSW, PWL, B365W, B365L
        -	3 sur l'elo, score arbitraire attribué à chaque joueur : elo_winner, elo_loser, proba_elo
        On observe que les données sont extraites par script sur un site public qui est toujours actif et à jour.
        Les données sont issues directement des résultats recensés par l'ATP, ce qui les rendent fiable, à l'exception des cotes des bookmakers et de l’elo.
        L'elo n'est pas une information officielle mais une donnée calculée selon la base du nombre de parties gagnées et perdues. 
        La base Confidence, contient des données calculées suite à l'exécution d'un modèle prédictif sur la base ATP. Il s'agit d'une approche proposée par le détenteur du notebook sur Kaggle, et nous choisissons de l'écarter de notre analyse dans un premier temps pour nous concentrer sur les données initiales.       
        """
    )

    st.markdown(
        """
        ### Stratégie 1 : Mettre en concurrence les cotes de plusieurs bookmakers sur un même pari de manière à être positif quel que soit le résultat
        """
    )

    fig1 = plt.figure(figsize=(14,7))
    plt.subplot(121)
    plt.scatter(x=df['B365L'],y=df['PSL'],color='red',marker='o')
    plt.xlabel("Cotes perdantes Pinnacle")
    plt.ylabel("Cotes perdantes B365")
    plt.title('Corrélation cote perdantes entre bookmakers')

    plt.subplot(122)
    plt.scatter(df['B365W'],df['PSW'],color='blue',marker='d')
    plt.xlabel("Cotes gagnantes Pinnacle")
    plt.ylabel("Cotes gagnantes B365")
    plt.title('Corrélation cote gagnantes entre bookmakers')
    st.pyplot(fig1)

    st.markdown(
        """
        ### Stratégie 2 : Pour un bookmaker donné, mettre en place une stratégie pour ne parier que sur les matchs avec un écart de cotes très élevés
        """
    )
    df_filtered = df.dropna()
    ecarts = np.arange(1,15,0.1)
    probas=[]
    for ecart in ecarts:
        small_psw_sum = df_filtered.PSW[df_filtered.PSL>ecart*df_filtered.PSW].sum()
        total_games = df_filtered.PSW[df_filtered.PSL>ecart*df_filtered.PSW] + df_filtered.PSL[df_filtered.PSW>ecart*df_filtered.PSL]
        proba = 100*(small_psw_sum - len(total_games)) /len(total_games)
        probas.append(proba)

    fig2 = plt.figure(figsize=(14,7))
    plt.plot(ecarts,probas)
    plt.title("Gains réalisés sur 100 parties à 1€ en pariant sur la cote la plus petite, variation par écart entre les cotes des 2 joueurs")
    plt.xlabel("écarts de cote entre les 2 joueurs")
    plt.ylabel("gains")
    st.pyplot(fig2)

    st.markdown(
        """
        ### Stratégie 3 : Evaluer les performances des joueurs pour déterminer la probabilité de victoire par joueur, sans considération des cotes des bookmakers
        """
    )
    fig3 = df.Winner.value_counts().nlargest(20).plot(kind='bar',title="Nombre de parties gagnées par joueurs").figure
    st.pyplot(fig3)


    fig4 = df.Loser.value_counts().nlargest(20).plot(kind='bar',title="Nombre de parties perdues par joueurs").figure
    st.pyplot(fig4)

    # Création du DataFrame df_player 
    # player
    # total play
    # wins
    # loses
    with st.spinner("Loading..."): 
        losers = df['Loser'].unique()
        winners = df['Winner'].unique()
        players = np.concatenate([losers,winners])
        players = np.unique(players)

        players_total_play = []
        players_wins = []
        players_loses = []
        players_odds = []

        for player in players : 
            players_total_play.append(len(df.loc[df['Winner']==player]) + len(df.loc[df['Loser']==player]))
            players_wins.append(len(df.loc[df['Winner']==player]))
            players_loses.append(len(df.loc[df['Loser']==player]))
            players_odds.append((df.loc[df['Winner']==player].B365W.mean() + df.loc[df['Loser']==player].B365L.mean())/2)


        d = {'player': players, 
            'games': players_total_play, 
            'wins':players_wins, 
            'loses':players_loses,
            'players_odds':players_odds}
        df_players = pd.DataFrame(data=d)
        df_players["ratio_win"] = df_players["wins"]/df_players["games"]
        figure5 = df_players.nlargest(20,"ratio_win").plot(kind='bar', y="ratio_win", x='player',title="Ratio victoires par parties").figure
        st.pyplot(figure5)


        data = df_players.nlargest(20,"games").sort_values("ratio_win",ascending=False)
        figure6 = plt.figure(figsize=(14,7))
        plt.bar(data.player, data.ratio_win)
        plt.title("Ratio victoires par parties pour les joueurs avec le plus grand nombre de match")
        plt.xticks(rotation='vertical')
        st.pyplot(figure6)

        # cote associée et rentabilité
        data = df_players.nlargest(20,"games").sort_values("ratio_win",ascending=False)
        figure7, ax1 = plt.subplots()
        ax1.bar(data.player, data.ratio_win)
        ax1.set_ylabel('% de parties gagnées')
        ax1.set_xticklabels(data.player, rotation='vertical')

        ax2 = ax1.twinx() 
        ax2.set_ylabel('cote moyenne des joueurs')
        ax2.plot(data.player, data.players_odds, color='red')

        figure7.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title("Ratio victoires par parties pour les joueurs avec le plus grand nombre de match")
        st.pyplot(figure7)