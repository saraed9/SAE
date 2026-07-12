# Spectra : Plateforme de billetterie sécurisée

## Contexte

Ce projet s'inscrit dans une SAE de sécurité informatique organisée en deux équipes : une équipe de développement (équipe bleue) chargée de concevoir un système d'information, et une équipe d'attaquants (équipe rouge) chargée de l'attaquer. Nous faisons partie de l'équipe bleue.

L'objectif était de développer un MVP (Minimum Viable Product) de vente de tickets de spectacles, en intégrant dès la conception les mesures de sécurité nécessaires pour contrer les risques classiques d'un système web : fuite de données, injection SQL, détournement de session, XSS, CSRF, brute force, déni de service, etc.

## Fonctionnalités du site

- Création de compte utilisateur (email, mot de passe, informations de facturation)
- Achat de tickets pour des spectacles (limite de 4 tickets par spectacle et par compte)
- Consultation des événements (date, prix, illustration)
- Dépôt d'avis et de notes sur les spectacles
- Génération de facture après achat
- Procédure de récupération de mot de passe oublié

## Stack technique

- **Backend** : Flask (Python)
- **Base de données** : PostgreSQL
- **Frontend** : HTML / CSS / JS (sans framework, volontairement minimal pour un MVP)

## Mesures de sécurité mises en place

### Injection SQL
- Utilisation exclusive de requêtes paramétrées / ORM (SQLAlchemy) : aucune concaténation de chaînes dans les requêtes SQL.
- Validation et typage stricts des entrées côté serveur avant toute requête.

### XSS (Cross-Site Scripting)
- Échappement automatique des templates Jinja2 (activé par défaut, non désactivé).
- Sanitisation des champs libres (avis, notes) avant stockage et avant affichage.
- Mise en place d'une politique de sécurité de contenu (Content-Security-Policy) pour limiter l'exécution de scripts non autorisés.

### CSRF (Cross-Site Request Forgery)
- Jetons CSRF (Flask-WTF / flask-seasurf) sur tous les formulaires modifiant des données (achat, avis, modification de compte).
- Vérification systématique de l'origine des requêtes sensibles.

### Détournement de session
- Cookies de session configurés en `HttpOnly`, `Secure`, `SameSite=Strict`.
- Régénération de l'identifiant de session à chaque connexion (protection contre la fixation de session).
- Expiration automatique des sessions inactives.

### Authentification et mots de passe
- Hachage des mots de passe avec bcrypt (jamais de mot de passe en clair, ni même en clair temporairement en mémoire au-delà du nécessaire).
- Politique de mot de passe robuste (longueur minimale, complexité).
- Procédure de récupération de mot de passe par lien à usage unique et durée de vie limitée, envoyé par email, sans jamais révéler si un email existe en base (pour éviter l'énumération de comptes).
- Protection contre le brute force : limitation du nombre de tentatives de connexion (rate limiting), verrouillage temporaire du compte.

### Fuite de données sensibles
- Chiffrement des données sensibles at rest (mots de passe hachés, informations de facturation minimisées).
- Principe de moindre privilège sur les accès à la base de données.
- Variables sensibles (clés secrètes, identifiants de base de données) gérées via fichier `.env`, jamais committées.

### Déni de service (DoS)
- Rate limiting sur les endpoints sensibles (connexion, achat, dépôt d'avis).
- Validation stricte des tailles de champs et de fichiers (illustrations) pour éviter les abus de ressources.

### Malware / Ransomware
- Aucun upload de fichier exécutable autorisé côté utilisateur.
- Validation stricte des types de fichiers pour les illustrations (whitelist d'extensions et vérification du contenu réel, pas seulement de l'extension).

## Approche générale

Chaque mesure ci-dessus a été pensée en réponse directe à un risque identifié en phase d'analyse (Phase 1), avant d'être implémentée en Phase 2/3. L'équipe pirate a ensuite testé ces protections, ce qui a permis d'ajuster certains points (durcissement supplémentaire des sessions et du rate limiting notamment).
