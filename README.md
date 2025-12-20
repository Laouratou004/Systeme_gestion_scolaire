# Systeme_gestion_scolaire
- Description du projet
Le Système de Gestion Scolaire est une application desktop développée en Python avec Tkinter, destinée à faciliter l’administration scolaire.
Elle permet de gérer les utilisateurs, étudiants, enseignants, matières et notes, tout en intégrant un système d’authentification sécurisé basé sur les rôles.
L’application est conçue pour répondre aux besoins des établissements scolaires souhaitant centraliser et sécuriser la gestion des données académiques.
- Objectifs
Mettre en place une base de données scolaire structurée
Développer une interface graphique intuitive
Implémenter un système d’authentification sécurisé
Gérer les rôles utilisateurs (Admin, Enseignant, Étudiant)
Permettre :
aux Administrateurs de gérer l’ensemble du système
aux Enseignants de saisir les notes
aux Étudiants de consulter leurs résultats
- Fonctionnalités
- Authentification
Connexion sécurisée avec nom d’utilisateur et mot de passe
Hachage des mots de passe (SHA-256 ou bcrypt)
Redirection automatique selon le rôle
👤 Gestion des rôles
Administrateur
Gestion des utilisateurs (CRUD)
Gestion des étudiants
Gestion des enseignants
Gestion des matières
Consultation globale des notes et statistiques
Enseignant
Visualisation des étudiants par matière
Saisie et modification des notes
Étudiant
Consultation des notes personnelles
Calcul automatique de la moyenne générale

🗄️ Modèle de Base de Données

Tables principales
Users
id
username
password
role
email
created_at

Students
id
first_name
last_name
birth_date
class

Teachers
id
first_name
last_name
specialty
Subjects
id
name
teacher_id

Grades
id
student_id
subject_id
grade
date

🛠️ Technologies utilisées
Composant	Technologie
Langage	Python 3
Interface graphique	Tkinter
Base de données	SQLite
Sécurité	SHA-256 / bcrypt
Versionnement	Git / GitHub

📁 Structure du projet
gestion-systeme-scolaire/
│
├── src/
│   ├── database/
│   │   └── database.py
│   ├── auth/
│   │   └── login.py
│   ├── admin/
│   ├── teacher/
│   ├── student/
│   └── utils/
│
├── main.py
├── README.md
├── .gitignore
