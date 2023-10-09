import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler,MinMaxScaler 
from sklearn.decomposition import PCA
from sklearn import ensemble
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import SelectKBest
from cachetools import cached
from sklearn.model_selection import train_test_split,cross_val_score

title = "Analyse en Composantes Principales"
sidebar_name = "Analyse en Composantes Principales"


def run():
    df = pd.read_csv("./../data_scrapped/training_dataset_init.csv")
    st.title(title)
    st.dataframe(df.head(10))
    #st.write(df.shape)
    st.dataframe(df.describe())
    #if st.checkbox("Afficher les NA") :
    #    st.dataframe(pd.DataFrame(df.isna().sum(), columns = ['features','count']))
    col_na=df.columns[df.isna().sum()!=0]
    data=df.dropna(subset=col_na,axis=0,how='any')
    target=data['winner_player1']
    data=data.drop(['match_id','match_date','player1_birthdate','player2_birthdate','player1_name','player2_name','winner_player1'],axis=1)
    # Séparation du jeu de donnée

    X_train,X_test,y_train,y_test=train_test_split(data,target,test_size=0.2,random_state=1234)
    # Choix du selecteur
    choix = ['Selecteur KBest', 'Selecteur Percentile']
    option = st.selectbox('Choix du selecteur', choix)
    st.write('Le selecteur choisi est :', option)
    if option == 'Selecteur KBest':
        selec=SelectKBest()
    elif option == 'Selecteur Percentile':
        display = st.radio('Quel percentile voulez-vous ?', ('20', '50','70','90'))
        if display == '20':
            selec=SelectPercentile(percentile=20)
        elif display == '50':
            selec=SelectPercentile(percentile=50)
        elif display == '70':
            selec=SelectPercentile(percentile=70)
        elif display == '90':
            selec=SelectPercentile(percentile=90)

    X_train_sel=selec.fit_transform(X_train,y_train)
    X_test_sel=selec.transform(X_test)
    scaler=StandardScaler().fit(X_train)
    X_train_scaled=scaler.transform(X_train)
    X_test_scaled=scaler.transform(X_test)
    scaler=StandardScaler().fit(X_train_sel)
    X_train_sel_scaled=scaler.transform(X_train_sel)
    X_test_sel_scaled=scaler.transform(X_test_sel)
    pca=PCA()
    X_train_pca=pca.fit_transform(X_train_sel)# PCA sans standardisation
    # Affichage de la part de variance expliquée
    # Refaire une PCA pour voir quels nombres d'axes 
    # pca = PCA(n_components = .9)
    pca1=PCA()
    X_train_pca=pca1.fit_transform(X_train_sel_scaled)# Avec standardisation
    fig = plt.figure()
    sns.set_style("darkgrid")
    plt.plot(pca1.explained_variance_ratio_.cumsum(),color='g',marker='o',linewidth=1.2)
    plt.xlim(0,X_train_pca.shape[1]-1)
    plt.xlabel("Nombre d'axes")
    plt.ylabel('Part de Variance expliquée')
    plt.title('Part de variance expliquée cumulée avec standardisation')
    plt.show()
    st.pyplot(fig)
    # Faire l'ACP avec le nombre d'axes choisit précedement ici n=5 pour avoir 90% de variance expliquée d'après le 2è graphique

    st.write("""#### Nuage de points""")
    pca=PCA(n_components=3)
    X_train_pca=pca.fit_transform(X_train_sel_scaled)
    # Transformation des données de X_test_var
    X_test_acp=pca.transform(X_test_sel_scaled)
    fig = plt.figure()
    fig = plt.figure(figsize=(20, 8))
    plt.subplot(121)
    plt.scatter(X_train_pca[:,0],X_train_pca[:,1],c=y_train,cmap='Spectral')
    plt.title("Nuage de points de l'ACP entre l'axe 1 et 2")
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    st.pyplot(fig)

    fig = plt.figure(figsize=(20, 8))
    plt.subplot(122)
    plt.scatter(X_train_pca[:,0],X_train_pca[:,2],c=y_train,cmap='Spectral')
    plt.title("Nuage de points de l'ACP entre l'axe 1 et 3")
    plt.xlabel('PCA1')
    plt.ylabel('PCA3')
    plt.show()
    st.pyplot(fig)


    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter=ax.scatter(X_train_pca[:,0],X_train_pca[:,1],X_train_pca[:,2],c=y_train, cmap='Spectral')
    fig.colorbar(scatter)
    ax.set_xlabel('PCA1')
    ax.set_ylabel('PCA2')
    ax.set_zlabel('PCA3')
    ax.set_title("Vue générale du nuage de points")
    st.pyplot(fig)

    option1 = st.radio('Choose the option', ['Logistic','KNN','SVM','RandomForest'])
    def Performance_PCA(model,color,label):
        score=[]
        if option == 'Selecteur KBest':
            selec=SelectKBest()
        elif (option == 'Selecteur Percentile')and display == '20':
            selec=SelectPercentile(percentile=20)
        elif (option == 'Selecteur Percentile')and display == '50':
            selec=SelectPercentile(percentile=50)
        elif (option == 'Selecteur Percentile')and display == '70':
            selec=SelectPercentile(percentile=70)
        elif (option == 'Selecteur Percentile')and display == '90':
            selec=SelectPercentile(percentile=90)

        X_train,X_test,y_train,y_test=train_test_split(data,target,test_size=0.2,random_state=1234)
        X_train_sel=selec.fit_transform(X_train,y_train)
        X_train_sel_scaled=scaler.transform(X_train_sel)
        for i in range(1,X_train_sel_scaled.shape[1]):
            X_train_sel=selec.fit_transform(X_train,y_train)
            X_test_sel=selec.transform(X_test)
            X_train_sel_scaled=scaler.transform(X_train_sel)
            X_test_sel_scaled=scaler.transform(X_test_sel)
            pca=PCA(n_components=i)
            X_train_pca=pca.fit_transform(X_train_sel_scaled)
            X_test_acp=pca.transform(X_test_sel_scaled)
            model.fit(X_train_pca,y_train)
            score.append(model.score(X_test_acp,y_test))
        st.markdown(
            """
            Représentation graphique du score en fonction de nombre d'axes k
            """
        )
        fig = plt.figure()
        plt.plot(score,color=color,linewidth=0.8,marker='.',label=label)
        plt.xlabel("Nombre d'axes conservés k")
        plt.ylabel('Score du modèle')
        plt.title("Performance du modèle en fonction du nombre d'axes conservés")
        plt.legend()
        st.pyplot(fig)
        st.write(model,"Nombres d'axes conservées:",np.argmax(score))
        st.write('Meilleur score:',score[np.argmax(score)])
    
    with st.spinner("Loading..."): 
        if option1 == 'Logistic':
            Performance_PCA(LogisticRegression(C=0.01778,penalty='l2',solver='lbfgs',random_state=123),color='orange',label='LogisticRegression')
        if option1 == 'SVM':
            Performance_PCA(SVC(kernel ='rbf'),label='SVM',color='red')
        if option1 == 'KNN':
            Performance_PCA(KNeighborsClassifier(n_neighbors=39),color='purple',label='KNN')
        if option1 == 'RandomForest':
            Performance_PCA(ensemble.RandomForestClassifier(max_features='sqrt',min_samples_split=2,random_state=123),color='green',label='RandomForest')