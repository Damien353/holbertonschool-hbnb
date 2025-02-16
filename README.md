# holbertonschool-HBnb - Documentation Technique
Projectt HBnB
## 1. Introduction
### 1.1 Objectif du document

The HBnB Evolution project aims to develop a simplified application inspired by Airbnb, allowing users to manage properties, leave reviews, and manage associated amenities. The first phase of the project focuses on creating technical documentation that will serve as the foundation for the system's design. This documentation will detail the overall architecture, business processes, and interactions between system entities, ensuring a clear understanding of the project. The goal is to lay the groundwork for scalable and flexible development.

### 1.2 Portée du Document

Ce document fournit une description détaillée de l’architecture technique du projet HBnB. Il est structuré en plusieurs sections, chacune couvrant un aspect clé du système :

📍**Architecture de Haut Niveau**:
Présentation de l’architecture en trois couches du système, accompagnée d’un diagramme de package expliquant la répartition des responsabilités et les interactions entre les composants. 

📍**Couche Logique Métier**:
Détails sur la conception des modèles et leurs relations, illustrés par un diagramme de classe.

📍**Flux d’Interaction des API**:
Analyse des interactions entre les couches via des diagrammes de séquence, mettant en évidence le traitement des requêtes utilisateurs.

📍**Explications et Justifications**: 
Chaque section est accompagnée de descriptions détaillées pour clarifier les choix de conception et assurer une compréhension globale du fonctionnement du système.

## 2. Architecture de Haut Niveau

### 2.1 Vue d'Ensemble

**HBnB suit une architecture à trois couches :**

📍**Couche de Présentation (Services API) :** Gère les interactions et requêtes des utilisateurs.

📍**Couche Logique Métier (Modèles & Façade) :** Gère la logique applicative et le traitement des données.

📍**Couche de Persistance (Accès à la Base de Données) :** Responsable du stockage et de la récupération des données.

### 2.2 Diagramme de Package de Haut Niveau

Le diagramme ci-dessous illustre la structure et les interactions entre ces couches :
![diagramme_package__720](https://github.com/user-attachments/assets/ae639521-ec0a-49d4-b84f-2c4e5bb07c0b)

### 2.3 Explication du Package de Haut Niveau

L'objectif premier de ce diagramme est d'avoir une vue d'ensemble du projet et de bien comprendre les correspondances entre les différentes couches.
Notre diagramme de Haut Niveau décrit les relations entre les trois couches de notre application. La première, PrésentationLayer, gère l'interface ainsi que les requêtes via une API. La couche métier applique les règles métier et centralise la gestion des données à travers une Facade et des modèles de données (User, Place, Review, Amenity). 
Enfin, la couche de persistance aussure la communication avec la base de données via des repositories et une interface d'accès aux données. Chaque couche est indépendante pour rendre le système clair et plus facile à modifier et entretenir. 
Le design se veut pyramidal. Il débute par la couche PrésentationLayer qui correspond à la couche la plus haute de notre projet. Chaque ligne montre les relations entre les éléments et les intéractions de l'utilisateur. Le diagramme présente les fonctionnalités principales. Les couleurs sont extraites de la charte graphique d'Airbnb. 

### 2.3 Explication du Modèle de Façade

Le Modèle de Façade simplifie les interactions entre les couches. Il sert d'interface entre la couche de présantation et la logique métier. Il permet de masquer la complexité du système. En centralisant les appels aux différents éntités, il évite une interaction directe avec la base de données ce qui répond à une logique d'encapsulation. Cela facilite la modularité, le fait que les couches soient bien séparées, ce qui facilite la maintenance et l'évolution du projet. Enfin cela facile les interactions car la couche de présentation n'interagit qu'avec une seule classe (Facade) au lieu de multiples classes métier.

## 3. Couche Logique Métier

### 3.1 Vue d'Ensemble

La Couche Logique Métier comprend les modèles principaux représentant les différentes entités dans HBnB, telles que les utilisateurs, les lieux, les avis et les commodités. Ces modèles encapsulent la logique nécessaire pour la validation, le traitement et l'interaction avec la base de données.

### 3.2 Diagramme de Classe pour la Logique Métier

DIAGRAMME A METTRE ICI LOGIQUE METIER

### 3.3 Explication

**Notre couche Logique Métier possède différents modèles:**

**Classe parente :**

Cette classe ** BaseModel** : Fournit des attributs communs (id, created_at, update_at) aux autres entités. Elle assure une meilleure cohérence des données et garantit une structure commune.

**Classes principales :**

📍**User :** Représente un utilisateur inscrit avec des détails d'authentification.

📍**Place :** Représente une unité locative avec des détails tels que l'emplacement et le prix. Elle gère également les équipements des logements.

📍**Review :** Contient les avis générés par les utilisateurs sur les lieux.

📍**Amenity :** Représente les commodités supplémentaires disponibles dans un lieu.


#### Relations :

- Un utilisateur possède plusieurs lieux.

- Un utilisateur rédige plusieurs avis.

- Un lieu reçoit plusieurs avis.

- Un lieu possède plusieurs commodités.

### 3.4 : Explication du diagramme: 

Ce diagramme de classes représente la structure et les interactions des principales entités du système de gestion des logements. Sa structure hiérarchique permet une bonne visualisation des relations entre ces classes. La classe parente centralise les attributs communs et garantit une cohérence des données. 
Les classes User, Place, Review, Amenity héritent de BaseModel et possèdent des propriétés et méthodes spécifiques. Un User peut créer plusieurs Places et rédiger des Review et avoir plusieurs Amenities. Le code couleur permet d'avoir plus de clarté sur le document et rappel la charte graphique d'Airbnb. 

## 4. Flux d'Interaction des API

### 4.1 Vue d'Ensemble

La couche API fournit une interface permettant aux utilisateurs d'interagir avec le système. L'API joue un rôle important en servant d'interface pour les demandes utilisateurs, comme l'enregistrement d'un utilisateur, la création d'un lieu, la soumission d'un avis ou la récupération de lieurx. 
Les diagrammes ci-dessous correspondent à chaque appel d'API :

### 4.2 Diagramme de séquence : Enregistrement d'utilisateur: 

DIAGRAMME A INSERER ICI 

#### 4.3 : Description du diagramme : 

L'utilisateur fournit ses informations à l'API via une requête POST/register. L'API valide les données, puis passe la demande à la façade, qui redirige la requête vers la logique métier pour l'insertion dans la base de données. Une fois l'utilisateur ajouté avec succès, l'API renvoie un identifiant utilisateur ou un message d'erreur.

#### 4.4 : Explication par étapes : 

- **1. Initiation de la requête par l'utilisateur (User):**
L'utilisateur envoie une requête HTTP POST /register au serveur, avec les informations nécessaires pour l'enregistrement : email, password, et name.
Cette étape marque le début du processus d'enregistrement de l'utilisateur dans le système. Les données envoyées par l'utilisateur sont envoyées sous forme de JSON dans le corps de la requête.
- **2. Traitement par l'API :**
Action : L'API reçoit la requête de l'utilisateur. Elle est responsable de la gestion de la communication avec le client (l'utilisateur) et de la validation des données.
L'API va transmettre les données à la Facade pour procéder à la validation.
- **3. Validation des données par la Facade:**
La Facade prend la responsabilité de valider les données d'entrée envoyées par l'utilisateur. Elle va vérifier si les informations sont correctes et complètes.
La Facade agit comme un intermédiaire, et c'est elle qui s'assure que les données sont prêtes pour être traitées dans la Business Logic.
- **4. Création de l'utilisateur par la Business Logic:**
Si la validation des données est réussie, la Facade transmet ces informations à la Business Logic. La logique métier gère la création de l'utilisateur dans le système. Elle peut, par exemple, vérifier si l'email est déjà utilisé, créer un nouveau compte pour l'utilisateur, etc.
- **5. Insertion des données dans la base de données (Database):**
La Business Logic envoie une requête SQL à la base de données pour insérer un nouvel enregistrement utilisateur. Cette requête peut être une instruction INSERT INTO users, qui ajoute les données dans la table users de la base de données. Cette étape consiste à enregistrer de manière permanente l'utilisateur dans la base de données pour qu'il puisse se connecter et interagir avec le système.
- **6. Réponse de la base de données à la Business Logic:**
La base de données renvoie une réponse à la Business Logic, soit un succès (si l'utilisateur a bien été créé) ou un échec (si une erreur est survenue, par exemple un email déjà existant).La Business Logic reçoit un retour du système de persistance pour savoir si l'action a été effectuée correctement ou non.
- **7. Retour du résultat à la Facade:**
Une fois l'utilisateur créé avec succès, la Business Logic renvoie l'ID de l'utilisateur créé à la Facade. La Facade obtient l'ID de l'utilisateur pour l'envoyer à l'API, permettant ainsi de donner un retour précis à l'utilisateur.
- **8. Réponse à l'API:**
La Facade transmet l'ID de l'utilisateur ou un message d'erreur (en cas d'échec de création) à l'API. Cette étape permet à l'API de préparer la réponse à l'utilisateur.
- **9. Réponse finale à l'utilisateur:**
L'API renvoie une réponse HTTP au client (l'utilisateur). Si la création de l'utilisateur a été un succès, elle renverra un code de statut HTTP 201 (créé) avec l'ID de l'utilisateur ou un message de succès. Si une erreur est survenue, l'API enverra un message d'erreur approprié (par exemple, email déjà utilisé, mot de passe trop faible, etc.). Cette réponse permet à l'utilisateur de savoir si son enregistrement a été réussi ou s'il y a eu un problème.

#### 4.5: Design du diagramme : 

Le diagramme montre ces interactions entre l'utilisateur, l'API et la classe Logique Métier et la Base de données. Il montre toutes les étapes pour l'enregistrement de cet utilisateur. Le système de flèches permet d'avoir une compréhension du système. Avec un système de design modulaire, les interactions entre les différentes couches sont plus claires et logiques. La lisibilité et la structure aide à la compréhension des étapes. 

### 4.6 : diagramme de séquence: Création d'un logement:

DIAGRAMME A METTRE ICI

#### 4.7: Description du diagramme :

L'utilisateur soumet une requête pour créer un lieu, le système valide et enregistre les informations dans la base de données, puis renvoie l'ID du lieu créé ou un message d'erreur.

### 4.8 : Description par étapes:

-1. **Initiation de la requête par l'utilisateur (User)**
L'utilisateur envoie une requête HTTP POST /register au serveur, avec les informations nécessaires pour l'enregistrement : email, password, et name. Cette étape marque le début du processus d'enregistrement de l'utilisateur dans le système. Les données envoyées par l'utilisateur sont envoyées sous forme de JSON dans le corps de la requête.
- **2. Traitement par l'API**
L'API reçoit la requête de l'utilisateur. Elle est responsable de la gestion de la communication avec le client (l'utilisateur) et de la validation des données.
L'API va transmettre les données à la Facade pour procéder à la validation.

- **3. Validation des données par la Facade**
La Facade prend la responsabilité de valider les données d'entrée envoyées par l'utilisateur. Elle va vérifier si les informations sont correctes et complètes (par exemple, si l'email est valide, si le mot de passe respecte certaines règles de sécurité, etc.). La Facade agit comme un intermédiaire, et c'est elle qui s'assure que les données sont prêtes pour être traitées dans la Business Logic.

- **4. Création de l'utilisateur par la Business Logic**
Si la validation des données est réussie, la Facade transmet ces informations à la Business Logic. La logique métier gère la création de l'utilisateur dans le système. Elle peut, par exemple, vérifier si l'email est déjà utilisé, créer un nouveau compte pour l'utilisateur, etc. La Business Logic assure l'intégrité et la cohérence des données avant de procéder à leur persistance dans la base de données.

- **5. Insertion des données dans la base de données (Database)**
La Business Logic envoie une requête SQL à la base de données pour insérer un nouvel enregistrement utilisateur. Cette requête peut être une instruction INSERT INTO users, qui ajoute les données dans la table users de la base de données. Cette étape consiste à enregistrer de manière permanente l'utilisateur dans la base de données pour qu'il puisse se connecter et interagir avec le système.

- **6. Réponse de la base de données à la Business Logic**
La base de données renvoie une réponse à la Business Logic, soit un succès (si l'utilisateur a bien été créé) ou un échec (si une erreur est survenue, par exemple un email déjà existant). La Business Logic reçoit un retour du système de persistance pour savoir si l'action a été effectuée correctement ou non.

-**7. Retour du résultat à la Facade**
Une fois l'utilisateur créé avec succès, la Business Logic renvoie l'ID de l'utilisateur créé à la Facade. La Facade obtient l'ID de l'utilisateur pour l'envoyer à l'API, permettant ainsi de donner un retour précis à l'utilisateur.
- **8. Réponse à l'API**
La Facade transmet l'ID de l'utilisateur ou un message d'erreur (en cas d'échec de création) à l'API. Cette étape permet à l'API de préparer la réponse à l'utilisateur.
 -**9. Réponse finale à l'utilisateur**
L'API renvoie une réponse HTTP au client (l'utilisateur). Si la création de l'utilisateur a été un succès, elle renverra un code de statut HTTP 201 (créé) avec l'ID de l'utilisateur ou un message de succès. Si une erreur est survenue, l'API enverra un message d'erreur approprié (par exemple, email déjà utilisé, mot de passe trop faible, etc.). Cette réponse permet à l'utilisateur de savoir si son enregistrement a été réussi ou s'il y a eu un problème.

### 4.9: Diagramme de séquence: créer une review

DIAGRAMME A METTRe

#### 4.10 : Description du diagramme:
L'utilisateur envoie une revue pour un lieu spécifique, qui est validée, insérée dans la base de données, puis l'ID de la revue est retourné à l'utilisateur.
### 4.11: Description par étapes :
Dans ce diagramme de séquence, la création d'une revue suit un processus en plusieurs étapes :
- **1.Utilisateur :**
Envoie une requête pour soumettre une revue pour un lieu avec les informations nécessaires (ID du lieu, ID de l'utilisateur, note, commentaire).
- **2.API :**
Reçoit la requête et transmet les données à la Facade pour validation.
- **3.Facade :**
Valide les données de la revue et les transmet à la Business Logic.
- **4.Business Logic :**
Gère la logique métier pour créer la revue et l'associe à l'utilisateur et au lieu.
- **5.Base de données :**
Insère la revue dans la table reviews et renvoie le résultat à la Business Logic.
- **6.Facade :**
Si la revue est validée, elle retourne l'ID de la revue à l'API.
- **7.API :**
Renvoie la réponse finale à l'utilisateur avec un statut de succès ou un message d'erreur en cas d'échec.

### 4.12: Diagramme de séquence: Récupération des lieux
DIAGRAMME A METTRE
#### 4:13 : Description du diagramme:
L'utilisateur demande la liste des lieux dans une ville donnée, le système récupère et renvoie les lieux correspondant à la ville spécifiée.

#### 4.14 : Description par étapes: 

Dans ce diagramme de séquence, la récupération des lieux dans une ville donnée suit un processus en plusieurs étapes :
-**1.Utilisateur :** 
Envoie une requête pour récupérer la liste des lieux dans une ville spécifique (ici, Rennes).
- **2.API :**
Reçoit la requête et transmet la ville à la Facade.
- **3.Facade :**
Demande à la Business Logic de récupérer les lieux correspondant à la ville spécifiée.
- **4.Business Logic :**
Effectue une requête dans la base de données pour récupérer les lieux correspondant à la ville.
- **5.Base de données :**
Renvoie la liste des lieux correspondant à la ville à la Business Logic.
- **6.Business Logic :**
Retourne la liste des lieux à la Facade.
- **7.Facade :**
Transmet la liste des lieux ou un message d'erreur à l'API.
- **8.API :**
Renvoie la réponse finale à l'utilisateur, avec la liste des lieux ou un message d'erreur en cas de problème.

## 5. Conclusion

Ce document sert de plan directeur pour le projet HBnB, garantissant la clarté de l'architecture et guidant l'implémentation. En suivant cette conception structurée, les développeurs peuvent assurer l'évolutivité, la lisibilité et la maintenabilité tout au long du cycle de vie du projet.

![diagramme_user_register_720](https://github.com/user-attachments/assets/04664916-8c48-4e29-b8cb-345140fd771e)
