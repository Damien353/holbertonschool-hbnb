# holbertonschool-HBnb - Documentation Technique
Projectt HBnB
## 1. Introduction
### 1.1 Objectif du document

The HBnB Evolution project aims to develop a simplified application inspired by Airbnb, allowing users to manage properties, leave reviews, and manage associated amenities. The first phase of the project focuses on creating technical documentation that will serve as the foundation for the system's design. This documentation will detail the overall architecture, business processes, and interactions between system entities, ensuring a clear understanding of the project. The goal is to lay the groundwork for scalable and flexible development.

### 1.2 Portée du Document

Ce document fournit une description détaillée de l’architecture technique du projet HBnB. Il est structuré en plusieurs sections, chacune couvrant un aspect clé du système :

Architecture de Haut Niveau : Présentation de l’architecture en trois couches du système, accompagnée d’un diagramme de package expliquant la répartition des responsabilités et les interactions entre les composants.
Couche Logique Métier : Détails sur la conception des modèles et leurs relations, illustrés par un diagramme de classe.
Flux d’Interaction des API : Analyse des interactions entre les couches via des diagrammes de séquence, mettant en évidence le traitement des requêtes utilisateurs.
Explications et Justifications : Chaque section est accompagnée de descriptions détaillées pour clarifier les choix de conception et assurer une compréhension globale du fonctionnement du système.

Le document couvre :

L'architecture globale du système à l'aide d'un diagramme de package de haut niveau.

La couche logique métier avec un diagramme de classe détaillé.

Le flux d'interaction des API illustré à travers des diagrammes de séquence.

Des notes explicatives pour justifier les décisions de conception et assurer la clarté.

## 2. Architecture de Haut Niveau

### 2.1 Vue d'Ensemble

HBnB suit une architecture à trois couches :

Couche de Présentation (Services API) : Gère les interactions et requêtes des utilisateurs.

Couche Logique Métier (Modèles & Façade) : Gère la logique applicative et le traitement des données.

Couche de Persistance (Accès à la Base de Données) : Responsable du stockage et de la récupération des données.

### 2.2 Diagramme de Package de Haut Niveau

Le diagramme ci-dessous illustre la structure et les interactions entre ces couches :
![diagramme_package__720](https://github.com/user-attachments/assets/ae639521-ec0a-49d4-b84f-2c4e5bb07c0b)

### 2.3 Explication du Modèle de Façade

Le Modèle de Façade simplifie les interactions entre les couches.

La Couche de Présentation communique uniquement avec la Façade dans la Couche Logique Métier.

La Couche Logique Métier abstrait les interactions complexes et communique avec la Couche de Persistance pour les transactions de données.

## 3. Couche Logique Métier

### 3.1 Vue d'Ensemble

La Couche Logique Métier comprend les modèles principaux représentant les différentes entités dans HBnB, telles que les utilisateurs, les lieux, les avis et les commodités. Ces modèles encapsulent la logique nécessaire pour la validation, le traitement et l'interaction avec la base de données.

### 3.2 Diagramme de Classe pour la Logique Métier

### 3.3 Explication

User : Représente un utilisateur inscrit avec des détails d'authentification.

Place : Représente une unité locative avec des détails tels que l'emplacement et le prix.

Review : Contient les avis générés par les utilisateurs sur les lieux.

Amenity : Représente les commodités supplémentaires disponibles dans un lieu.

Relations :

Un utilisateur possède plusieurs lieux.

Un utilisateur rédige plusieurs avis.

Un lieu reçoit plusieurs avis.

Un lieu possède plusieurs commodités.

## 4. Flux d'Interaction des API

### 4.1 Vue d'Ensemble

La couche API fournit une interface permettant aux utilisateurs d'interagir avec le système. Le diagramme ci-dessous démontre un processus de demande de réservation.

### 4.2 Diagramme de Séquence et appel API

### 4.3 Explication

La Couche de Présentation envoie une requête.

La Couche Logique Métier valide et traite la demande.

La Couche de Persistance interagit avec la base de données pour vérifier la disponibilité et enregistrer les détails de la réservation.

Une confirmation est envoyée à l'utilisateur.
## 5. Conclusion

Ce document sert de plan directeur pour le projet HBnB, garantissant la clarté de l'architecture et guidant l'implémentation. En suivant cette conception structurée, les développeurs peuvent assurer l'évolutivité, la lisibilité et la maintenabilité tout au long du cycle de vie du projet.

![diagramme_user_register_720](https://github.com/user-attachments/assets/04664916-8c48-4e29-b8cb-345140fd771e)
