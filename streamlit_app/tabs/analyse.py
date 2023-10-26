import streamlit as st
#Optimisation 
st.cache_data
st.cache_resource
st.cache(allow_output_mutation=True)

import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from datetime import datetime,timedelta
import seaborn as sns

title = "Exploration des données et visualisation des données"
sidebar_name = "Jeu de données et webscraping"


def run():
    df = pd.read_csv("./../data_scrapped/co_uk_data.csv", low_memory=False)
    st.title(title)

    st.markdown(
        """
        ## Compréhension des données
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
        ### Proportion des NaN
        """
        )
    missing=(round(df.isnull().sum()/len(df),4)*100).sort_values(ascending = False)
    missing_df = pd.DataFrame({'Pourcentage des valeurs manquantes': missing})
    st.dataframe(missing_df)


    st.write ("Les données manquantes sont donc principalement des matchs sans cotes.Elles restent utiles pour déterminer le profil par joueur, il est donc préférable de garder ces données.")
    st.write("A noter également que notre base ne comporte pas de données dupliquées")

    st.markdown(
        """
        ## Stratégies

        Plusieurs hypothèses sont posées:  
        1 - Mettre en concurrence les cotes de plusieurs bookmakers sur un même pari de manière à être positif quel que soit le résultat 

        2 - Pour un bookmaker donné, mettre en place une stratégie pour ne parier que sur les matchs avec un écart de côtes très élevés 

        3 - Evaluer les performances des joueurs pour déterminer la probabilité de victoire par joueur, et le corréler aux cotes des bookmakers pour assurer un retour sur investissement

        """
    )


    ############################################################################################
                                    #Stratégie1#
    ############################################################################################
    st.markdown(
        """
        ### Stratégie 1 : Mettre en concurrence les cotes de plusieurs bookmakers sur un même pari de manière à être positif quel que soit le résultat

        Le but de cette approche est de déterminer si, pour un même pari, la cote des bookmakers s’oppose de telle manière que parier simultanément sur les deux garantirait un bénéfice.
        """
    )
    df2=df[['ATP', 'Best of', 'WRank', 'LRank','PSW','PSL', 'B365W', 'B365L', 'elo_winner', 'elo_loser', 'proba_elo' ]]
    fig=plt.figure(figsize=(24, 28))
    plt.subplot(311)
    sns.heatmap(df2.corr(), annot=True, cmap='bwr', vmin=-1, vmax=1, square=True, linewidths=0.5)
    plt.title('Forte corrélation entre les cotes des bookmakers en notre possession B365W/PSW vs B365L/PSL (R² > 90%)')
    st.pyplot(fig)

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



    ############################################################################################
                                    #Stratégie2#
    ############################################################################################
    st.markdown(
        """
        ### Stratégie 2 : Pour un bookmaker donné, mettre en place une stratégie pour ne parier que sur les matchs avec un écart de cotes très élevés

        Le but de cette stratégie serait de déterminer si, pour bookmaker donné, le fait de parier uniquement sur les matchs avec un écart de cotes élevés, permettrait de prédire au mieux la probabilité d’un joueur gagnant un match. 
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
    #plt.savefig(fig2, dpi=500)


    ############################################################################################
                                    #Stratégie3#
    ############################################################################################
    st.markdown(
        """
        ### Stratégie 3 : Evaluer les performances des joueurs pour déterminer la probabilité de victoire par joueur, sans considération des cotes des bookmakers
        Cette stratégie est plus complexe et se divise en deux parties : 

        - Prédire en utilisant les données propres aux joueurs (classement mondial, nombre de sets gagnés, nombre de points avant le tournois...) et les conditions du tournois (type de surface, de séries) le vainqueur du match.  

        - Vérifier que la cote associée à chaque pari réussi permet un retour sur investissement  

        En tenant en compte le fait que le tennis se dispute entre deux joueurs ayant des conditions de jeu identique, notre analyse se porte sur les axes suivants : 

        """
    )

    ############## Création du DataFrame df_player 
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

        surface_win_hard = []
        surface_win_clay = []
        surface_win_grass = []
        surface_win_carpet = []
        surface_loss_hard = []
        surface_loss_clay = []
        surface_loss_grass = []
        surface_loss_carpet = []

        for player in players : 
            winner_values = df.loc[df['Winner']==player]["Surface"].value_counts() 
            if hasattr(winner_values, 'Hard'):
                surface_win_hard.append(winner_values.Hard)
            else:
                surface_win_hard.append(0)

            if hasattr(winner_values, 'Clay'):
                surface_win_clay.append(winner_values.Clay)
            else:
                surface_win_clay.append(0)

            if hasattr(winner_values, 'Grass'):
                surface_win_grass.append(winner_values.Grass)
            else:
                surface_win_grass.append(0)

            if hasattr(winner_values, 'Carpet'):
                surface_win_carpet.append(winner_values.Carpet)
            else:
                surface_win_carpet.append(0)
            

            loser_values = df.loc[df['Loser']==player]["Surface"].value_counts() 
            if hasattr(loser_values, 'Hard'):
                surface_loss_hard.append(loser_values.Hard)
            else:
                surface_loss_hard.append(0)

            if hasattr(loser_values, 'Clay'):
                surface_loss_clay.append(loser_values.Clay)
            else:
                surface_loss_clay.append(0)

            if hasattr(loser_values, 'Grass'):
                        surface_loss_grass.append(loser_values.Grass)
            else:
                surface_loss_grass.append(0)

            if hasattr(loser_values, 'Carpet'):
                surface_loss_carpet.append(loser_values.Carpet)
            else:
                surface_loss_carpet.append(0)

        df_players["surface_win_hard"] = surface_win_hard
        df_players["surface_win_clay"] = surface_win_clay
        df_players["surface_win_grass"] = surface_win_grass
        df_players["surface_win_carpet"] = surface_win_carpet
        df_players["surface_loss_hard"] = surface_loss_hard
        df_players["surface_loss_clay"] = surface_loss_clay
        df_players["surface_loss_grass"] = surface_loss_grass
        df_players["surface_loss_carpet"] = surface_loss_carpet

        df_players["surface_win_hard_ratio"] =(df_players.surface_win_hard / (df_players.surface_win_hard + df_players.surface_loss_hard))-0.5
        df_players["surface_win_clay_ratio"] = (df_players.surface_win_clay / (df_players.surface_win_clay + df_players.surface_loss_clay))-0.5
        df_players["surface_win_grass_ratio"] = (df_players.surface_win_grass / (df_players.surface_win_grass + df_players.surface_loss_grass))-0.5
        df_players["surface_win_carpet_ratio"] = (df_players.surface_win_carpet / (df_players.surface_win_carpet + df_players.surface_loss_carpet))-0.5
        df_players["ratio_win"] = df_players["wins"]/df_players["games"]

                # Est ce que l'écart de rank est significatif sur le résultat du match ?
        ecarts = np.arange(1,10,0.2)
        probas=[]
        matchs=[]
        for ecart in ecarts:
            best_rank_win = df.loc[(df['WRank']*ecart)<(df['LRank'])]['WRank'].count()
            best_rank_loss = df.loc[(df['LRank']*ecart)<(df['WRank'])]['WRank'].count()
            proba = 100*best_rank_win /(best_rank_win+ best_rank_loss)
            match = best_rank_win + best_rank_loss
            matchs.append(match)
            probas.append(proba)

        ############## Affichage des graphes

        fig3 = df.Winner.value_counts().nlargest(20).plot(kind='bar',title="Nombre de parties gagnées par joueurs").figure
        fig4 = df.Loser.value_counts().nlargest(20).plot(kind='bar',title="Nombre de parties perdues par joueurs").figure
        fig5 = df_players.nlargest(20,"ratio_win").plot(kind='bar', y="ratio_win", x='player',title="Ratio victoires par parties").figure

        def affichage(axe):
            if axe == 'Ratio de parties gagnées au nombre de matchs':
                
                with st.spinner("Loading..."):
                    tab1, tab2 = st.tabs(["Nombre de parties gagnées/perdues par joueurs","Ratio victoires par parties"])
                    with tab1:

                        st.pyplot(fig3)
                        
                        st.pyplot(fig4)
                    with tab2:
                        
                        st.pyplot(fig5)

                        # cote associée et rentabilité
                        data = df_players.nlargest(20,"games").sort_values("ratio_win",ascending=False)
                        fig7, ax1 = plt.subplots()
                        ax1.bar(data.player, data.ratio_win)
                        ax1.set_ylabel('% de parties gagnées')
                        ax1.set_xticklabels(data.player, rotation='vertical')
                        ax2 = ax1.twinx() 
                        ax2.set_ylabel('cote moyenne des joueurs')
                        ax2.plot(data.player, data.players_odds, color='red')

                        fig7.tight_layout()  # otherwise the right y-label is slightly clipped
                        plt.title("Ratio victoires par parties pour les joueurs avec le plus grand nombre de match")
                        st.pyplot(fig7)


            elif axe == 'Influence de la surface':
                with st.spinner("Loading..."):
                    tab1, tab2 = st.tabs(["Répartition par type de surface", "Ratio victoires par type de surface "])
                    with tab1:
                        # Use the Streamlit theme.
                        # This is the default. So you can also omit the theme argument.
                        fig8=plt.figure(figsize=(6,5))
                        plt.pie(df['Surface'].value_counts(),labels=df['Surface'].value_counts().index, autopct="%.1f%%", explode = [0, 0, 0, 0.2],)
                        title="Répartition par type de surface"
                        st.pyplot(fig8)
                    with tab2:
                        # Use the native Plotly theme.
                        fig9=df_players.nlargest(20,"games").plot(kind='bar', 
                        y=["surface_win_hard_ratio","surface_win_clay_ratio","surface_win_grass_ratio","surface_win_carpet_ratio"] , x='player',
                        title="Ratio victoires (-0.5 0.5) par type de surface pour les 20 premiers joueurs au nombre de parties").figure
                        st.pyplot(fig9)

            elif axe == 'Influence du court':
                with st.spinner("Loading..."):
                    fig10=plt.figure(figsize=(4,3))
                    plt.pie(df['Court'].value_counts(),labels=df['Court'].value_counts().index, autopct="%.1f%%")
                    st.pyplot(fig10)


            elif axe == 'Analyse des victoires par tournoi':
                with st.spinner("Loading..."):
                    #tab1, tab2 = st.tabs(["Répartition par type de tournoi","Nombre de victoires par tournoi"])
                    #with tab1:
                    #    fig11=plt.figure(figsize=((8,6)))
                    #    plt.pie(df['Series'].value_counts(),labels=df['Series'].value_counts().index, autopct="%.1f%%") 
                    #    st.pyplot(fig11)

                    #with tab2:             
                    fig12 = plt.figure(figsize=(14,8))
                    plt.subplot(121)
                    data=df[df.Winner.isin(df.Winner.value_counts().nlargest(10).index.values)]\
                    [df.Tournament.isin(['Australian Open','Wimbledon','US Open','French Open','Masters Cup'])]
                    sns.countplot(x='Winner',hue='Tournament',data=data)
                    plt.xticks(rotation=80)
                    plt.ylabel('Nombre de Victoires')
                    plt.title('Nombre de victoires du top 10 sur les tournois majeurs')

                    plt.subplot(122)
                    data=pd.concat([df.Winner,df.Tournament],axis=1).groupby('Winner').value_counts().nlargest(20)
                    data.plot(kind='bar',color='orange',edgecolor='red')
                    plt.title('Les plus grandes victoires des 20 meilleurs joueurs par tournoi')
                    plt.xlabel('')
                    plt.ylabel('Nombre de tournoi')
                    st.pyplot(fig12)
                        
            elif axe == 'Différence de rang ATP entre les joueurs':
                with st.spinner("Loading..."): 
                    best_rank_win = df.loc[df['WRank']<df['LRank']]['WRank'].count()
                    total_match = df.WRank.count()

                    print(round(100*best_rank_win /total_match,2), "% des joueurs qui ont un meilleur rank ATP gagnent le match") 
                    fig_atp, ax1 = plt.subplots()
                    ax1.set_xlabel('écarts de rank ATP entre les 2 joueurs')
                    ax1.set_ylabel('nombre de matchs') 
                    ax1.bar(ecarts, matchs)
                    ax2 = ax1.twinx() 
                    ax2.set_ylabel('% de Victoires')
                    ax2.plot(ecarts, probas, color='red')

                    fig_atp.tight_layout()  # otherwise the right y-label is slightly clipped
                    plt.title("influence du rank ATP sur la victoire")
                    #plt.savefig('C:/Users/gmari/.vscode/figures', dpi=500)
                    st.pyplot(fig_atp)


        choix = ['Ratio de parties gagnées au nombre de matchs', 'Influence de la surface', 'Analyse des victoires par tournoi', 'Différence de rang ATP entre les joueurs']
        option = st.selectbox("Choix d'axe d'analyse", choix)

        with st.spinner("Loading..."):
            affichage(option)

        st.markdown(
            """
            ## Conclusion

            L'approche basée sur la performance des joueurs pour déterminer le résultat des matchs  est la plus sérieuse et la plus prometteuse. 

            L’analyse des données associées permettent de confirmer l’influence de plusieurs feature à notre disposition sur le résultat, ce qui est encourageant

            """
        )
