Nom du projet : Nianaboli

Description :
Réalisation d’une application console permettant aux utilisateurs de gérer et partager efficacement leurs dépenses collaboratives. 

Fonctionnalités :
Inscription 
authentification 
Création de groupe 
Ajout de membre 
Création de dépenses 
Répartition de dépenses (manuellement et  automatiquement)
Notifications 
Suppression de groupe 
Suppression de membres 
Suppression de dépenses 
Modification de dépense 
Modification de groupe 
Paiement 
Statistiques global de l’application 
Déconnexion 
Visualiser un groupe 
Lister ses groupes 
Lister ses dépenses 

Installation :
Pour cloner le projet 
Ouvrez le git Bash
Saisissez la commande svte:
git clone
Suivi du lien du dépôt :
https://github.com/mohdiop/nianaboli.git

Utilisation

Pour lancer notre application il faut ouvrir un console et exécuter le fichier main.py
Ensuite vous serez redirigé sur un espace de bienvenue avec trois options :
Inscription 
Connexion 
Déconnexion 
Quitter 
Quand tu cliques sur l'option 1 (connexion) on te demande de renseigner ton numéro donc si tu est déjà inscrit on te demande encore de renseigner ton mot de passe qui est la connexion sans pour autant être inscrit on te renvoie un message d’utilisateur introuvable.
Quand tu cliques sur l’option 2(inscription) on te demande de renseigner les champs suivants :
Nom: qui n’accepte pas de valeur nulle
Prénom: qui n’accepte pas de valeur nulle 
Téléphone :qui commence par (7,8,9,6,5) et qui est égal à 8 chiffres 
Mot de passe : qui doit être composé au moins d’un majuscule,d’un minuscule,d’un chiffre et d' un caractère spécial et qui doit être supérieur ou égal à 6 caractères.
Quand l'utilisateur s’inscrit ou s’authentifie il sera dirigé sur son espace qui offre les options suivantes :
Créer un groupe 
Voir ses notifications 
Visualiser ses groupes 
Quand l’utilisateur choisit l’option 1 (créer un groupe) il lui sera demandé de renseigner le nom du groupe,et il lui sera demandé s’il veut ajouter un membre à son groupe il devra répondre par oui ou non et pourra y ajouter autant de membres à force de choisir oui et quand à un non il sera renvoyé à la page précédente 
Quand l'utilisateur choisira l’option 2(Visualiser ses groupes) il aura deux options :
Soit visualiser ses groupes créés 
Soit visualiser les groupes dans lesquels il est membre 
En visualisant ses groupes il peut:
Lister les dépenses du groupes(En listant les dépenses l’utilisateur peux decider de visualiser une dépense en particulier et ainsi faire un paiement visualiser un paiement,et l’administrateur lui étant là bas peux valider un paiement)
Ajouter des membres(étant administrateur)
Créer, supprimer ou modifier une dépense (Seul l’ administrateur du groupe en a le droit)

Quand l'utilisateur choisit l'option 3(Notifications) il pourra voir toutes ses notifications 
Quand l’utilisateur choisit l’option 4(déconnecter) il quitte la session et doit obligatoirement se connecter



Technologie utilisée :

Python : version 3.13.3

dbrowser: SQLite 3 

Contributeurs :

Mohamed Diop

Niakalen Diakité 

Djènèba Haïdara

Ibrahim Mahamadou

Aboubacar Sogoba 

Amadou Bakayoko

Mohamed Touré

Daba Diallo 




