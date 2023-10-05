import streamlit as st


title = "Paris sportif - tennis"
sidebar_name = "Introduction"


def run():

    # TODO: choose between one of these GIFs
    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    #st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    #st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        Ce projet a pour objectif de proposer une rentabilité positive lors de paris sportif sur le tennis. Le jeu de donnée fourni l'intégralité des matchs recensés par l'ATP depuis 2001 est fourni, ainsi que les cotes initiales proposées par plusieurs bookmakers. Notre travail consistera à analyser les données et proposer des stratégies à rendement fiable.
        Ce projet se déroulera donc en 2 temps, à savoir :
        - Une étape d'exploration, de visualisation.
        - Un pré-traitement des données et un modèle prédictif suggérant les cotes à jouer à une date t de telle manière que le retour sur investissement soir positif.
        """
    )
