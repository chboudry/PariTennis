import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import StandardScaler,MinMaxScaler 
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from cachetools import cached
import shap
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import train_test_split

title = "Interprétabilité"
sidebar_name = "Interprétabilité"


def run():
    df = pd.read_csv("./../data_scrapped/training_dataset_init.csv")
    col_na=df.columns[df.isna().sum()!=0]
    data=df.dropna(subset=col_na,axis=0,how='any')
    target=data['winner_player1']
    data=data.drop(['match_id','match_date','player1_birthdate','player2_birthdate','player1_name','player2_name','winner_player1'],axis=1)
    X_train,X_test,y_train,y_test=train_test_split(data,target,test_size=0.2,random_state=1234)
    selec=SelectKBest()
    X_train_sel=selec.fit_transform(X_train,y_train)
    X_test_sel=selec.transform(X_test)
    scaler=StandardScaler().fit(X_train)
    X_train_scaled=scaler.transform(X_train)
    X_test_scaled=scaler.transform(X_test)
    scaler=StandardScaler().fit(X_train_sel)
    X_train_sel_scaled=scaler.transform(X_train_sel)
    X_test_sel_scaled=scaler.transform(X_test_sel)
    st.title(title)

    st.write("#### Précision du modèle")
    rl_opt=LogisticRegression ( max_iter=2000,random_state=22, C=0.01778279410038923, solver="lbfgs")
    model_lr= rl_opt.fit(X_train_sel_scaled, y_train)

    #tableau des  probabilités pour les joueurs  d'appartenir à la classe 0 ou la classe 1
    probs = rl_opt.predict_proba(X_test_sel_scaled)
    y_preds = np.where(probs[:,1]>0.4,1,0)
    #
    cm = pd.crosstab(y_test, y_preds, rownames=['Classe réelle'], colnames=['Classe prédite'])
    print(cm)

    #courbe ROC  - outil très efficace pour évaluer un modèle
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, seuils=roc_curve(y_test,probs[:,1] , pos_label=1)
    roc_auc = auc(fpr, tpr)
    fig = plt.figure()
    plt.plot(fpr, tpr, color='purple', lw=2, label='Modèle clf (auc = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Aléatoire (auc = 0.5)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taux faux positifs')
    plt.ylabel('Taux vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc="lower right")
    plt.show()
    st.pyplot(fig)

    st.markdown("""
        L'AUC ROC de notre modèle se situe bien au-dessus de celui d'un modèle non-informatif et en-dessous de celui d'un modèle parfait. Avec 76% d'AUC ROC, on en déduit que notre modèle est  assez performant.  
        """
    )
    

    #Calcul de l'importance des features
    df.match_date = df.match_date.apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))
    #dictionnaire = {'player1_birthdate':'datetime64',
    #                'player2_birthdate':'datetime64'}
    #st.write(dictionnaire)
    #df_new = df.astype(dictionnaire)
    df_new = df
    #création des variables year "année du match" et month "mois du match" pour faciliter plus tard le calcul de la moyenne mobile
    df_new["year"] = df_new['match_date'].dt.year
    df_new["month"] = df_new['match_date'].dt.month

    #suppression det toute ligne ayant des valeurs manquantes
    df_new = df_new.dropna()

    df_new = df_new[(df.player1_plays > 6) & (df.player2_plays>6)]
    print(df_new.shape)
    df_new.head(2)
    X = df_new[[ "player1_name", "player1_age", "player1_atprank", "player1_plays", "player1_wins", "player1_losses", "player1_elo", "player1_mean_serve_rating", 
                "player1_height", "player1_weight", "player1_oddsB365",
            "player2_name","player2_age", "player2_atprank", "player2_plays", "player2_wins", "player2_losses", "player2_elo", "player2_mean_serve_rating", 
            "player2_height", "player2_weight", "player2_oddsB365",         "match_date"]]
    #Stockage la variable cible "winner_player1" dans une variable y
    y = df_new.winner_player1

    #Création d'un ensemble d'entraînement et d'un ensemble de tests
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,random_state=101)
    col_to_drop = [ "match_date","player2_name","player1_name"]
    X_train = X_train.drop(col_to_drop,axis=1)
    X_test= X_test.drop(col_to_drop,axis=1)

    #Pour les variables ayant des valeurs avec une étendue [0,1] ==> usage de la méthodes MinMax.
    MinMax = MinMaxScaler()
    col_to_minmax = ["player1_plays", "player1_wins", "player1_losses","player1_elo",
                        "player2_plays","player2_wins", "player2_losses", "player2_elo"]

    X_train[col_to_minmax] = MinMax.fit_transform(X_train[col_to_minmax])
    X_test[col_to_minmax] = MinMax.transform(X_test[col_to_minmax])

    # Pour le reste des variables, nous utilisons la méthodes StandardScaler
    scaler = StandardScaler()
    col_to_std_scale = ["player1_age", "player1_atprank", "player1_elo", "player1_mean_serve_rating", "player1_height", "player1_weight", "player1_oddsB365",
            "player2_age", "player2_atprank", "player2_elo", "player2_mean_serve_rating",  "player2_height", "player2_weight", "player2_oddsB365",]

    X_train[col_to_std_scale] = scaler.fit_transform(X_train[col_to_std_scale])
    X_test[col_to_std_scale] = scaler.transform(X_test[col_to_std_scale])

    X_train_scaler = pd.DataFrame(X_train)
    X_test_scaler = pd.DataFrame(X_test)
    rl_opt=LogisticRegression( max_iter=2000,random_state=22, C=0.01778279410038923, solver="lbfgs")
    model_lr= rl_opt.fit(X_train_scaler, y_train)
    coefficients=rl_opt.coef_
    avg_importance=np.mean(np.abs(coefficients), axis=0)
    feature_importance=pd.DataFrame({'Feature':X_train_scaler.columns, 'Importance':avg_importance})
    feature_importance=feature_importance.sort_values('Importance',ascending=True)
    feature_importance.plot(x='Feature', y='Importance', kind='barh', figsize=(10,6))
    # Calcul de l'importance des features
    coefficients=rl_opt.coef_
    avg_importance=np.mean(np.abs(coefficients), axis=0)
    feature_importance=pd.DataFrame({'Feature':X_train_scaler.columns,'Importance':avg_importance})
    feature_importance=feature_importance.sort_values('Importance',ascending=True)
    fig = plt.figure()
    sns.barplot(y='Feature', x='Importance',orient='h',data=feature_importance)
    plt.title("Niveau d'importance des features obtenues avec la régression logistique")
    st.pyplot(fig)
    st.dataframe(feature_importance.sort_values(by='Importance', ascending=False).head(8))
    keep=['player1_age', 'player1_atprank',  'player1_oddsB365', 'player2_age',  'player2_plays', 'player2_wins', 'player2_losses',  'player2_oddsB365']

    X_train_new=X_train_scaler[keep]
    X_test_new=X_test_scaler[keep]

    #Arbre de décision
    # st.markdown("""
    # Interprétabilité du modèle : "arbre de décision"
    #             """)
    # from sklearn.tree import DecisionTreeClassifier
    # tree_clf_final = DecisionTreeClassifier(criterion ='entropy', max_depth=3, random_state=123)

    # #entrainement du modèle
    # tree_clf_final.fit(X_train_new, y_train)

    # feat_importances = pd.Series(tree_clf_final.feature_importances_, index=X_train_new.columns)
    # feature_importances=feat_importances.sort_values(ascending=True)
    # fig = plt.figure()
    # feat_importances.nlargest(8).plot(kind='barh');
    # st.pyplot(fig)
    # st.markdown("""
    #     L'arbre de décision suggère que les côtes du Bookmaker suffirait pour prédire le vainqueur du tournoi.
    #     """
    # )

    #Interprétabilité classique - PCA avec la selection des variables pertinentes
    n = X_train_new.shape[1]
    pca=PCA(n_components = 2)
    data_2D=pca.fit_transform(X_train_new)
    data_2D_test=pca.transform(X_test_new)

    coeff = pca.components_.transpose()
    xs = data_2D[:, 0]
    ys = data_2D[:, 1]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())

    rl_final=LogisticRegression ( max_iter=2000,random_state=22, C=0.01778279410038923, solver="lbfgs")
    rl_final.fit(X_train_new,y_train)
    # principalDf = pd.DataFrame({'PC1': xs*scalex, 'PC2': ys * scaley})
    # y_train_pred = rl_final.predict(X_train_new)
    # finalDF = pd.concat([principalDf, pd.Series(y_train_pred, name='Winner')], axis=1)

    # plt.figure(figsize=(18, 16))
    # sns.scatterplot(x='PC1', y='PC2', hue='Winner', data=finalDF, alpha=0.5)

    # for i in range(n):
    #     plt.arrow(0, 0, coeff[i, 0]*1, coeff[i, 1]*1,  color='k', alpha=0.5,  head_width=0.01,)
    #     plt.text(coeff[i, 0]*1, coeff[i, 1] * 1, X_train_scaler.columns[i], color='blue')

    # plt.xlim(-0.8,0.8)
    # plt.ylim(-0.8, 0.8)

    #Interprétabilité SHARP
    scaler = StandardScaler()
    X_train_scaler = pd.DataFrame(X_train)
    X_test_scaler = pd.DataFrame(X_test)
    keep=['player1_age', 'player1_atprank', 'player1_elo', 'player1_weight', 'player1_oddsB365', 'player2_age', 'player2_atprank', 'player2_plays', 'player2_wins', 'player2_losses', 'player2_height', 'player2_weight', 'player2_oddsB365']
    X_train_new=X_train_scaler[keep]
    X_test_new=X_test_scaler[keep]
    explainer = shap.LinearExplainer(rl_opt,X_train_scaler,nsamples=1000, feature_perturbation=None)
    shap_values = explainer.shap_values(X_test_scaler)

    print('Expected Value:', explainer.expected_value)
    #Importance obtenu avec SHARP
    rl_final=LogisticRegression ( max_iter=2000,random_state=22, C=0.01778279410038923, solver="lbfgs") 
    rl_final.fit(X_train_new,y_train)

    explainer = shap.LinearExplainer(rl_final,X_train_new,nsamples=1000, feature_perturbation=None)
    shap_values = explainer.shap_values(X_test_new)
    #fig = plt.figure()
    #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28,10))
    fig1 = plt.figure(figsize=(28,20))
    shap.summary_plot(shap_values, X_test_new, plot_type="bar")
    plt.title("Importance des features avec SHARP")
    st.pyplot(fig1)

    fig2 = plt.figure(figsize=(28,20))
    shap.summary_plot(shap_values, X_test_new)
    plt.title("Graphe de densité des features")
    st.pyplot(fig2)

    st.markdown("""
    Les cotes, l'age et le rang ATP des joueurs ont plus de poids lors de la prédiction du vainqueur du match (voir le graphique de densité à droite)
            """
    )
