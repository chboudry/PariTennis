import streamlit as st
import pandas as pd
import numpy as np
import graphviz
from PIL import Image


title = "Graph Neural Network"
sidebar_name = "Graph Neural Network"


def run():

    st.title(title)

    st.markdown(
        """
        ### Des données inexploitées ? 
        Aucun des modèles étudiés ne permette d'analyser en profondeur les relations entre joueur.
        Que pouvons nous faire avec les graphes ?
        """
    )

    st.graphviz_chart('''
    digraph {
        "Raphael Nadal" -> "Karol Kucera"
        "Raphael Nadal" -> "Albert Costa"
        "Guillermo Coria" -> "Raphael Nadal"
        "Guillermo Coria" -> "Juan Ignacio Chela"
        "Guillermo Coria" -> "Carlos Moya"
        "Carlos Moya" -> "Julien Boutter"
        "Carlos Moya" -> "Tommy Robredo"
        "Tommy Robredo" -> "Juan Ignacio Chela"
        "Juan Ignacio Chela" -> "Olivier Rochus"
        "Alberto Martin" -> "Olivier Rochus"
        "Alberto Martin" -> "Albert Costa"
        "Albert Costa" -> "Sargis Sargsian"
        "Gustavo Kuerten" -> "Sargis Sargsian"
        "Alberto Martin"  -> "Gustavo Kuerten"
        "Guillermo Coria" -> "Alberto Martin" 
    }
    ''')

    st.markdown(
        """
        On choisit de représenter les joueurs par des noeuds et les matchs par des edges. La direction de l'edge indique le vainqueur.
        Sur le graphe ci dessus, on observe par example que G. Costa gagne contre C. Moya, qui lui même gagne contre T. Robredo, qui lui même gagne contre J.I. Chela.  
        Par relation de Chasles, est il raisonnable de penser que G. Coria gagnerait contre J.I. Chela ? Dans cet exemple, c'est le cas.  
        Il reste à determiner si c'est statistiquement fiable et pouvoir l'exploiter dans un modèle.
        """
    )

    st.markdown(
        """
        ### Quelques concepts
        """
    )

    image = Image.open('./assets/graph_problems.png')
    st.image(image, caption='Source: DeepFindr Youtube Videos')

    st.markdown(
        """
        Dans le cas de notre pari tennis, notre objectif est de réaliser la prédiction de direction d'edge (ou de manière équivalente une prédiction de feature sur un undirected graph).
        """
    )

    image = Image.open('./assets/simple_graph.png')
    st.image(image, caption='Source: DeepFindr Youtube Videos')

    st.markdown(
        """
        On associe des features à chaque node, les edge sont représentés par une matrice d'adjacence.  
        Par la suite, La matrice d'adjacence ne sera pas utilsée directement, le modèle prendra directement en entrée une liste de vector décrivant les edges.
        """
    )

    image = Image.open('./assets/message_passing_layers.png')
    st.image(image, caption='Source: DeepFindr Youtube Videos')

    st.markdown(
        """
        Pour que les noeuds soient influencés par leurs voisins, on utilise la technique du message passing layer.  
        Cette technique dispose de multiples variantes, selon les informations que l'on souhaite prendre en compte, et l'importance que l'on souhaite leur attribuer. 
        """
    )

    image = Image.open('./assets/edge_weight.png')
    st.image(image, caption='Source: DeepFindr Youtube Videos')

    st.markdown(
        """
        Dans ce dernier exemple, l'edge est composé d'une unique feature (que l'on appelle alors le poids) qui influencera la transformation appliquée au noeud par son voisin.
        """
    )


    st.markdown(
        """
        ### Mise en pratique
        Il convient de déterminer quel features peuvent être placés sur les nodes et quels autres sur les edges.
        """
    )


    st.graphviz_chart('''
    digraph {
        fontname="Helvetica,Arial,sans-serif"
        node [fontname="Helvetica,Arial,sans-serif"]
        edge [fontname="Helvetica,Arial,sans-serif"]
        graph [fontsize=30 labelloc="t" label="" splines=true overlap=false rankdir = "LR"];
        ratio = auto;
        "Guillermo Coria" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Guillermo Coria</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Carlos Moya" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Carlos Moya</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Tommy Robedro" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Tommy Robedro</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Juan Ignacio Chela" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Juan Ignacio Chela</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Guillermo Coria" -> "Carlos Moya"
        "Carlos Moya" -> "Tommy Robedro"
        "Tommy Robedro" -> "Juan Ignacio Chela" 
        "Guillermo Coria" -> "Juan Ignacio Chela"
        label="Premier modèle avec 2 node features uniquement, accuracy à 50%"
    }
    ''')

    st.graphviz_chart('''
    digraph {
        fontname="Helvetica,Arial,sans-serif"
        node [fontname="Helvetica,Arial,sans-serif"]
        edge [fontname="Helvetica,Arial,sans-serif"]
        graph [fontsize=30 labelloc="t" label="" splines=true overlap=false rankdir = "LR"];
        "Guillermo Coria" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Guillermo Coria</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Carlos Moya" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Carlos Moya</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Tommy Robedro" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Tommy Robedro</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Juan Ignacio Chela" [ style = "filled, bold" penwidth = 5 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">Juan Ignacio Chela</font></td></tr><tr><td align="left" port="r0">Taille</td></tr><tr><td align="left" port="r1">Poids</td></tr></table>> ];              
        "Guillermo Coria" -> "Carlos Moya"
        "Carlos Moya" -> "Tommy Robedro" 
        "Tommy Robedro" -> "Juan Ignacio Chela" 
        "Guillermo Coria" -> "Juan Ignacio Chela" [ penwidth = 5 fontsize = 28 fontcolor = "black" label = "Rank ATP / Odds" ];
        label="Second modèle avec 4 edge features : accuracy à 57%"
    }
    ''')

    st.markdown(
        """
        ### What next ? : 
        - Représentation des données
          - comment représenter le rank ATP ? 
        - Comment gérer le batching ? 
        - Comment gérer la temporalité ? 
        """
    )