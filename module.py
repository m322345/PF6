#########################################################################################################
#                                Modules utilisées dans le Projet 7 OC                                  #
#########################################################################################################

# imports
import os, sys, time
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

randomState = 42

def repartitionCibles(dataset):
    """
    Calcule le ratio des valeurs cibles
    _______________entrées_______________
    dataset : array des valeurs 
    _______________sorties_______________
    affiche le pourcentage de positifs
    """
    if not isinstance(dataset, pd.DataFrame):
        dataset = pd.DataFrame(dataset, columns = ['TARGET'])
    if 'TARGET' in dataset.columns:
        values = dataset['TARGET'].value_counts()
        val1 = values[1] / len(dataset['TARGET'])
        print("Ratio des valeurs cibles")
        print(f"valeurs positives {val1:.1%} ({values[1]})")
        print(f"valeurs négatives {(1-val1):.1%} ({values[0]})")
    else:
        print("Le dataset fourni ne comporte pas de cibles")




def matriceConfusion(y_reel, y_pred, titre):
    """
    Calcule les valeurs et pourcentages et
    Affiche une matrice de confusion avec 
    les données envoyées
    _______________entrées_______________
    y_reel : array des valeurs réélles
    y_pred : array des valeurs prédites
    titre  : titre affiché sur le graphe
    _______________sorties_______________
    affiche le graphe de la matrice de confusion
    """
    plt.figure(figsize=(4, 3))
    matrice = metrics.confusion_matrix(y_reel, y_pred)
    noms_groupes = ['Vrai Neg','Faux Pos','Faux Neg','Vrai Pos']
    vals_groupes = ["{0:0.0f}".format(value) for value in matrice.flatten()]
    perc_groupes = ["{0:.2%}".format(value) for value in matrice.flatten()/np.sum(matrice)]
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(noms_groupes,vals_groupes,perc_groupes)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(matrice,
                annot=labels,
                fmt='',
                cmap=plt.cm.YlOrBr,
                cbar=False)
    plt.title(f'Matrice de confusion: {titre}', pad=20)
    plt.ylabel('Classe réelle')
    plt.xlabel('Classe prédite')
    plt.show()
"""
import importlib 
importlib.reload(module)

y_pred_proba = log_reg_train > 0.1
y_pred_proba = np.array(y_pred_proba > 0)*1
module.matrice_confusion(train_labels, y_pred_proba, "Regression Logistique")    """



def encoderVariables(train, test):
    le = LabelEncoder()
    le_count = 0
    # Iterate through the columns
    for col in train:
        if train[col].dtype == 'object':
            # If 2 or fewer unique categories
            if len(list(train[col].unique())) <= 2:
                # Train on the training data
                le.fit(train[col])
                # Transform both training and testing data
                train[col] = le.transform(train[col])
                test[col] = le.transform(test[col])
                # Keep track of how many columns were label encoded
                le_count += 1
    # one-hot encoding of categorical variables
    train = pd.get_dummies(train, dummy_na= True)
    test = pd.get_dummies(test, dummy_na= True)
    # alignement des données
    train_labels = train['TARGET']
    # Align the training and testing data, keep only columns present in both dataframes
    train, test = train.align(test, join = 'inner', axis = 1)
    # Add the target back in
    train['TARGET'] = train_labels
    return train, test



def netoyAugmtDonnées(dataset):
    """
    Nettoie les données du dataset et 
    ajoute de nouvelles features
    _______________entrées_______________
    dataset : array
    _______________sorties_______________
    retourne le dataset nettoyé avec nouvelles features
    """
    # traite les valeurs aberrantes
    dataset['DAYS_EMPLOYED_ANOM'] = dataset["DAYS_EMPLOYED"] == 365243
    dataset['DAYS_EMPLOYED'].replace({365243: np.nan}, inplace = True)

    # création de features
    dataset['CREDIT_INCOME_PERCENT'] = dataset['AMT_CREDIT'] / dataset['AMT_INCOME_TOTAL']
    dataset['ANNUITY_INCOME_PERCENT'] = dataset['AMT_ANNUITY'] / dataset['AMT_INCOME_TOTAL']
    dataset['CREDIT_TERM'] = dataset['AMT_ANNUITY'] / dataset['AMT_CREDIT']
    dataset['DAYS_EMPLOYED_PERCENT'] = dataset['DAYS_EMPLOYED'] / dataset['DAYS_BIRTH']
    dataset['CREDIT_INCOME_BY_AGE'] = dataset['CREDIT_INCOME_PERCENT'] / dataset['DAYS_BIRTH']
    dataset['ANNUITY_INCOME_BY_AGE'] = dataset['ANNUITY_INCOME_PERCENT'] / dataset['DAYS_BIRTH']
    dataset['INCOME_TO_FAMILYSIZE'] = dataset['AMT_INCOME_TOTAL'] / dataset['CNT_FAM_MEMBERS']
    return dataset



def equilibrageDonnées(dataset, labels):
    smt = SMOTE(random_state=randomState)
    dataset_res, labels_res = smt.fit_resample(dataset, labels)
    return dataset_res, labels_res



def traitementDonnées(dataset_train, dataset_test, smote=True):
    """
    Traite les données du dataset
    _______________entrées_______________
    dataset : array
    train : (0/1) traitement specifique train
    _______________sorties_______________
    X_train: jeu d'entrainement
    X_test: jeu de test
    labels: labels du jeu d'entrainement
    features: liste des features
    """
    temps_debut = time.time()
    print('----------- Datas before traitments ----------')
    repartitionCibles(dataset_train)
    print('..............................................')
    print('Training data shape: ', dataset_train.shape)
    print('Testing data shape: ', dataset_test.shape)
    dataset_train = netoyAugmtDonnées(dataset_train)
    dataset_test = netoyAugmtDonnées(dataset_test)
    dataset_train, dataset_test = encoderVariables(dataset_train, dataset_test)
    # Drop the target from the training data
    labels = dataset_train['TARGET']
    X_train = dataset_train.drop(columns = ['TARGET'])
    # Copy of the testing data
    X_test = dataset_test.copy()
    # Feature names
    features = list(X_train.columns)
    # Median imputation of missing values
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    imputer.fit(X_train) # Fit on the training data
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)
    # Scale each feature to 0-1
    scaler = MinMaxScaler(feature_range = (0, 1))
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    if smote == True:
        print('------------- application SMOTE --------------')
        X_train, labels = equilibrageDonnées(X_train, labels)
    print('----------- Datas after traitments -----------')
    repartitionCibles(labels)
    print('..............................................')
    print('Training data shape: ', X_train.shape)
    print('Testing data shape: ', X_test.shape)
    print('------------- Time of traitments -------------')
    temps_total = time.time() - temps_debut
    print(f'Time: {temps_total:.3}s')
    return X_train, X_test, labels, features



