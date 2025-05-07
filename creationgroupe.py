import models, createUser, connexion, administrateur
from datetime import datetime

def creationGroupe(user: models.UtilisateurInfo):
    print("--------------- Création  de groupe ---------------")
    print("\n")
    nom = input("Le nom de votre groupe de dépense : ")
    groupe = user.creerGroupe(nom)

    choix = int(input("Voulez-vous ajouter un membre? (1 = oui/ 2 = non)\n"))

    while (choix == 1):
        telephone = input("Le numéro du membre à ajouter : ")
        membre = createUser.getUserByTel(telephone)
        if(membre is None):
            print("Utilisateur introuvable!\n")
        else: 
            ajoutMembre = models.Appartenance(
                membre.id,
                groupe.id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                models.Role.MEMBRE
            )
            values = (ajoutMembre.idUtilisateur, ajoutMembre.idGroupe, ajoutMembre.dateAjout, "MEMBRE")
            connexion.cursor.execute("INSERT INTO appartenance (idUtilisateur, idGroupe, dateAjout, role) VALUES (?, ?, ?, ?)", values)
        choix = int(input("Voulez-vous ajouter un membre? (1 = oui/ autres chiffres = non)\n"))
    administrateur.userGroups(user)