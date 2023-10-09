import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime,timedelta
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

title = "Modèles"
sidebar_name = "Modèles"


def run():

    st.title(title)

    st.markdown(
        """
        ### Préparation des données
        """
    )

    st.markdown(
        """
        Le jeu de donnée tel que récupéré ne permet pas l'exploitation de modèle car il n'y a pas de colonne cible à prédire.
        """
    )

    df=pd.read_csv("./../data_scrapped/co_uk_data.csv",low_memory=False)
    st.write(df)

    st.markdown(
        """
        Ci dessous notre jeu de donnée modifié avec les données issus du scrapping, et un traitement pour obtenir une feature cible : winner_player1.  
        On répond à la question : le joueur 1 a t'il gagné ? Oui = 1, Non = 0  
        Notre jeu de données est parfaitement équilibré car nous avons nous même créer le dataset et 50% des matchs sont gagnés par le joueur 1.
        """
    )

    df=pd.read_csv("./../data_formatted/training_dataset.csv",low_memory=False)
    st.write(df)

    st.markdown(
        """
        ### Entrainement du modèle et méta paramètres
        """
    )
    playsnumber = st.slider('Minimal number of plays by player', 0, 12, 6)

    options = st.multiselect(
        'Feature selection',
        ['atprank', 'age', 'plays', 'wins', 'losses', 'elo', 'mean_serve_rating', 'mean_atp_adversary', 'height', 'weight', 'oddsB365'],
        ['atprank', 'age', 'plays', 'wins', 'losses', 'elo', 'mean_serve_rating', 'mean_atp_adversary', 'height', 'weight', 'oddsB365'])

    dynamic_features = []
    for option in options :
            featurep1="player1_" + option
            featurep2="player2_" + option
            dynamic_features.append(featurep1)
            dynamic_features.append(featurep2)

    static_features = ["player1_name", "player2_name", "match_date"]
    needed_features = ["player1_oddsB365", "player2_oddsB365"]

    features=[]
    if "oddsB365" not in options:
        features = static_features + dynamic_features + needed_features
    else :
        features = static_features + dynamic_features

    df = df.dropna()
    df = df[(df.player1_plays > playsnumber) & (df.player2_plays>playsnumber)]
    X = df[features]
    y = df.winner_player1

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)

    col_to_drop =[]
    if "oddsB365" not in options:
        col_to_drop = ["player1_name", "player2_name", "match_date", "player1_oddsB365", "player2_oddsB365"]
    else:
        col_to_drop = ["player1_name", "player2_name", "match_date"]
    X_train_filtered = X_train.drop(col_to_drop,axis=1)
    X_test_filtered = X_test.drop(col_to_drop,axis=1)

    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.3,max_depth=1, random_state=0)
    model = model.fit(X_train_filtered, y_train)

    y_predict = model.predict(X_test_filtered)
    y_predict_proba = model.predict_proba(X_test_filtered)
    percentageaccuracy = accuracy_score(y_predict, y_test)
    text = f"**Accuracy : {percentageaccuracy:.4f}**"
    st.markdown(text)

    ### affichage match 
    df_roi = X_test.copy()
    df_roi["y_predict_proba"] = y_predict_proba[:,0]   #all rows, first column = prediction score for winner 1 
    df_roi["y_predict"] = y_predict
    df_roi["y_test"] = y_test

    df_roi["proba_bookmaker"] = 1/df_roi.player2_oddsB365
    st.write(df_roi[["player1_name","player2_name","y_predict", "y_test","y_predict_proba","proba_bookmaker"]])


    st.markdown(
        """
        ### Calcul du retour sur investissement
        On peut ici aussi appliquer des stratégies pour décider sur quels matchs parier.
        """
    )
    playsnumber = st.slider('Confidence', 0.0, 1.0, 0.0, 0.1)
    predict_proba_above_predict_bookmaker = st.checkbox('Confidence above bookmaker', value= False)

    df_roi = X_test.copy()
    df_roi["y_predict_proba"] = y_predict_proba[:,0]   #all rows, first column = prediction score for winner 1 
    df_roi["y_predict"] = y_predict
    df_roi["y_test"]=y_test
    df_roi["proba_bookmaker"] = 1/df_roi.player2_oddsB365

    total_match = df_roi.shape[0]
    df_roi= df_roi.loc[df_roi["y_predict_proba"]>playsnumber]
    if predict_proba_above_predict_bookmaker == True:
        df_roi= df_roi.loc[df_roi["y_predict_proba"]>df_roi["proba_bookmaker"]]

    money_invested=round(df_roi.shape[0],2)

    money_won = 0.0
    for index, row in (df_roi[y_predict == y_test]).iterrows():
        if row.y_predict == 0 :
            money_won += row.player2_oddsB365
        else:
            money_won += row.player1_oddsB365

    money_spent = money_invested
    money_won = round(money_won,2)
    total = round(money_won - money_invested, 2)
    ROI = round(money_won*100/money_invested,2)

    html_str = f"""
    <style>
    p.a {{
    font: bold 12px Courier;
    }}
    </style>
    <table>
    <tr>
        <td>Total matchs</th>
        <td>{total_match}</th>
    </tr>
    <tr>
        <td>Money invested (1€ per match played)</td>
        <td>{money_invested}€</td>
    </tr>
    <tr>
        <td>Money won</td>
        <td>{money_won}€</td>
    </tr>
    <tr>
        <td>Total</td>
        <td>{total}€</td>
    </tr>
    <tr>
        <td>ROI</td>
        <td>{ROI}%</td>
    </tr>
    """
    
    st.markdown(html_str, unsafe_allow_html=True)

    st.markdown("""
        ### Modèles testés
        """
    )

    html_str = f"""
    <style>
    p.a {{
    font: bold 12px Courier;
    }}
    </style>
    <table>
    <tr>
        <th>Modèles évalués</th>
        <th>Accuracy (test)</th>
        <th>ROI</th>
    </tr>
    <tr>
        <td>Logistic regression</td>
        <td>71.35%</td>
        <td>92.57%</td>
    </tr>
    <tr>
        <td>Logistic regression with moving average</td>
        <td>61.37%</td>
        <td>77.12%</td>
    </tr>
    <tr>
        <td>KNN</td>
        <td>67.58%</td>
        <td>76.72%</td>
    </tr>
    <tr>
        <td>Decision Tree</td>
        <td>69.40%</td>
        <td>75.54%</td>
    </tr>
    <tr>
        <td>Random Forest</td>
        <td>66.86%</td>
        <td>75.54%</td>
    </tr>
        <tr>
        <td>Gradient Boosting</td>
        <td>68.97%</td>
        <td>94.12%</td>
    </tr>
    <tr>
        <td>SVM</td>
        <td>67.90%</td>
        <td>77.11%</td>
    </tr>
    <tr>
        <td>SVM with moving average</td>
        <td>68.11%</td>
        <td>77.12%</td>
    </tr>
        <tr>
        <td>Dense Neural Network</td>
        <td>68.11%</td>
        <td>75.16%</td>
    </tr>
    """

    st.markdown(html_str, unsafe_allow_html=True)



    st.markdown(
        """
        ### Premières conclusions
        - La plupart des modèles plafonnent à 70% d'accuracy, ce qui s'avère insuffisant pour obtenir un ROI positif 
        - L'ajout de nouvelles features via le web scrapping apporte des performances marginales au modèle, les features les plus pertinentes sont déjà présentes.  
        - De manière assez paradoxale, il a été observé que des modèles avec précisions moindre obtenaient un ROI plus élevé. On peut supposer que l'alignement du modèle sur la cote des bookmakers provoquent un style de jeu très prudent qui implique de très faibles gains en cas de victoire et des pertes élevées en cas de défaites. 
        - A performance égale, il est plus judicieux de retenir l'un des modèles les plus simple à expliquer, comme la régression logistique par exemple.  
        """
    )