import streamlit as st
import pandas as pd
import numpy as np


title = "Conclusion"
sidebar_name = "Conclusion"


def run():

    st.title(title)

    st.markdown(
        """
        L' utilisation des features fournies dans le dataset initial nous permet très vite d'obtenir une accuracy de l'ordre de 70% avec des modèles simples. En revanche, malgré cette précision, le retour sur investissement reste négatif.  

        L'interprétabilité des modèles réalisés nous permet d'identifier que la cote des joueurs est un des plus grands facteurs d'influence pour notre classification binaire : nous sommes alors alignés sur la prédiction du bookmaker, qui nous fait gagner certes 70% du temps, mais nous fait perdre davantage en 30% de défaites.  
        
        Sans cette cote, nos modèles descendent à 65% de précision et l'on observe que cette précision n'est pas suffisante pour garantir un retour sur investissement.  
    
        A ce stade, plusieurs stratégies peuvent êtres implémentés : faut-il parier contre le bookmaker : fort gain a faible fréquence ; ou parier avec lui : faible gain à forte fréquence.  

        En appliquant le modèle sur certains matchs uniquement (confidence du modèle, nombres de matchs minimums pour les joueurs...), plutôt que sur l'ensemble, on parvient de temps en temps à un retour positif, mais le nombre de parties jouées est alors marginal, tout comme le gain, et nos critères de sélections ne résistent pas aux validations croisées. 

        In fine il revient d'abord de connaitre le gagnant du match, et si la cote nous permet de gagner 5%, mieux vaut ne pas l'exclure. Le reste de notre temps sera consacré à un travail de webscrapping pour ajouter de nombreuses features aux modèles, ainsi que l'étude de nombreux autres modèles.  

        Dans notre dernier modèle le plus abouti, nous noterons notamment que l'âge des joueurs est le facteur de 3ème importance, alors que celui-ci n'était pas présent dans notre jeu de données initial. 

        Enfin, certaines pistes comme le graph neural network semble très prometteuses car elles permettent une meilleure représentation des relations entre joueurs dont les autres modèles sont incapables. Sujet complexe qui aurait mérité un mois supplémentaire pour en voir son aboutissement. 

        De manière générale, le projet pari qui nous a été proposé nous a permis une approche progressive du Machine Learning, puis une montée en complexité au fur et à mesure des nouveaux modèles étudiés. Nous avons pu mettre en pratique tous les éléments du cours et nous en affranchir avec nos propres analyses et modèles. 
        """
    )