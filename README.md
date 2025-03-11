![Entete](images/projet.png)

# 📌 Implémentation d’un Modèle de Scoring Crédit et Optimisation du Système MLOps

## 📖 Contexte
L’entreprise **Prêt à Dépenser**, spécialisée dans le crédit à la consommation, souhaite développer un **modèle de scoring** afin d’évaluer la probabilité qu’un client rembourse son prêt. 

L’objectif est de concevoir un **algorithme de classification** capable de **prédire le risque de défaut de paiement** et d’industrialiser son déploiement via une approche **MLOps**.

l’**industrialisation complète du cycle de vie du modèle** nécessite d’intégrer une solution de **suivi des performances en production**.

L’objectif est d’utiliser la librairie **Evidently** pour **détecter le Data Drift**, garantissant ainsi que le modèle reste performant face aux nouvelles données.


## 🎯 Objectifs du Projet
- ✅ Construire un **modèle de scoring crédit** basé sur des données clients.
- ✅ Analyser la **feature importance** globale et locale.
- ✅ Mettre en place une **API** pour exposer le modèle en production.
- ✅ Implémenter une **approche MLOps** pour automatiser l’intégration et le suivi du modèle.
- ✅ Déployer l’**API du modèle de scoring** dans le cloud.
- ✅ Mettre en place une **interface utilisateur** permettant de tester l’API.
- ✅ Intégrer **Evidently** pour surveiller le **Data Drift** entre les données d’entraînement et celles en production.
- ✅ Préparer une **présentation structurée** expliquant la démarche et les choix techniques.

## 🛠️ Étapes du Projet

### 1️⃣ **Préparation de l’Environnement MLOps**
- Configuration de **MLFlow** pour le suivi des expérimentations.
- Mise en place d’un **model registry** pour la gestion des modèles.
- Gestion du code avec **Git & GitHub Actions** pour CI/CD.

### 2️⃣ **Préparation et Feature Engineering des Données**
- Exploration des **données clients et comportementales**.
- Nettoyage et préparation des variables pour la modélisation.
- Gestion du **déséquilibre des classes** (bons vs mauvais payeurs).

### 3️⃣ **Optimisation et Entraînement des Modèles**
- Définition d’un **score métier** pour pénaliser différemment les erreurs de classification.
- Sélection et entraînement des modèles via **GridSearchCV**.
- Comparaison des performances avec des métriques comme **AUC et accuracy**.

### 4️⃣ **Analyse et Explicabilité du Modèle**
- Étude de la **feature importance** avec SHAP/LIME.
- Visualisation des contributions des variables aux prédictions.

### 5️⃣ **Déploiement et Industrialisation**
- Exposition du modèle via une **API REST** (Flask/FastAPI).
- Déploiement sur une **solution cloud gratuite**.
- Création d’une **interface Streamlit** pour tester l’API.

### 6️⃣ **Déploiement de l’API dans le Cloud**
- Versionner le code avec **Git**.
- Automatiser le déploiement avec **GitHub Actions**.
- Héberger l’API sur une **solution Cloud gratuite** (Heroku, Render, AWS, etc.).

### 7️⃣ **Création d’une Interface de Test pour le Scoring**
- Développer une **interface utilisateur avec Streamlit**.
- Connecter l’interface à l’**API de scoring**.
- Permettre la soumission de données et l’affichage des résultats du modèle.

### 8️⃣ **Surveillance du Data Drift avec Evidently**
- Comparer les distributions des features entre :
  - `application_train` (données d’entraînement)
  - `application_test` (nouvelles données clients en production)
- Générer un **rapport HTML Evidently** pour visualiser les dérives.
- Détecter les features les plus sujettes au **Data Drift**.

### 9️⃣ **Présentation du Projet**
- Structurer une **présentation claire** des choix méthodologiques.
- Justifier les décisions sur le **modèle, son déploiement et le suivi en production**.

## 📦 Livrables Attendus
- ✅ Un **notebook** contenant l’analyse exploratoire et l’implémentation du modèle.
- ✅ Un **modèle de scoring optimisé** et stocké via MLFlow.
- ✅ Une **analyse des variables explicatives** et de leur impact sur la décision.
- ✅ Un **pipeline MLOps** assurant le suivi et la mise à jour du modèle.
- ✅ Une **API déployée** et accessible en ligne pour prédire la probabilité de défaut.
- ✅ Une **interface utilisateur fonctionnelle** permettant de tester le scoring.
- ✅ Un **rapport Evidently** sur le Data Drift entre les données d’entraînement et de production.
- ✅ Une **présentation détaillée** expliquant le cycle de vie du modèle et le suivi MLOps.

## 🚀 Objectif Final
Fournir un **outil automatisé et interprétable** permettant d’évaluer le risque de crédit, tout en garantissant un **suivi rigoureux des performances** du modèle grâce aux pratiques **MLOps**.

Assurer un **déploiement robuste et un suivi efficace** du modèle de scoring, permettant à l’entreprise d’**anticiper les dérives des données et d’ajuster le modèle en conséquence**.

## Descriptif de la structure :

repertoire			| description
------------------- | -----------
.github/workflows 	| Le Workflow github qui vient lancer les tests unitaires à chaque push du projet
Api 				| Le code de l'Api qui est déployée automatiquement vers Render lors d'un push
Appli				| L'application frontend déployée automatiquement vers Streamlit
tests				| Les tests unitaires réalisés avec Pytest

Le fichier Modelisation.ipynb contient l'exploration, les tests de modélisations sauvegardées vers Mlflow et la modélisation finale.

## Les outils :

- [Dashboard Render](https://dashboard.render.com/)
- [API hébergée sur Render](https://ocp7-api.onrender.com/)
- [Test de l'API hébergée sur Render](https://ocp7-api.onrender.com/docs/)
- [Application hébergée sur Streamlit](https://ocp7-froidure.streamlit.app/)

---
- 👥 **Compétences requises** : Machine Learning, Python, MLOps, API, CI/CD, MLOps, Python, API, CI/CD, Streamlit, Evidently.
- 🌍 **Technologies** : GitHub Actions, Cloud Deployment, Monitoring MLOps.
- 🌍 **Source des données** : Issues du site Kagle [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)
