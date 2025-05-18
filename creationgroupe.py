import models, createUser, connexion, utilisateur, os, style
from datetime import datetime

def creationGroupe(user: models.UtilisateurInfo):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Création de groupe")
    nom = input("Le nom de votre groupe de dépense : ")
    groupe = user.creerGroupe(nom)

    choix = int(input("Voulez-vous ajouter un membre? (1 = oui/ 2 = non)\n"))

    while (choix == 1):
        telephone = input("Le numéro du membre à ajouter : ")
        membre = createUser.getUserByTel(telephone)
        if(membre is None):
            print("Utilisateur introuvable!\n")
        elif(telephone == user.telephone):
            print("Vous êtes déjà l'administrateur de ce groupe!")
        elif(isAllreadyAMember(membre.id, groupe.id)):
            print("Ce membre a déjà été ajouté!")
        else: 
            ajoutMembre = models.Appartenance(
                membre.id,
                groupe.id,
                f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}",
                models.Role.MEMBRE
            )
            values = (ajoutMembre.idUtilisateur, ajoutMembre.idGroupe, ajoutMembre.dateAjout, "MEMBRE")
            connexion.cursor.execute("INSERT INTO appartenance (idUtilisateur, idGroupe, dateAjout, role) VALUES (?, ?, ?, ?)", values)
            notification = models.Notification(
                "Nouveau groupe",
                f"Vous avez été ajouté au groupe {groupe.nom} par {user.prenom} {user.nom}",
                f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"
            )
            connexion.cursor.execute("INSERT INTO notification (titre, contenu, date) VALUES (?, ?, ?)", (notification.titre, notification.contenu, f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"))
            notification.setId(connexion.cursor.lastrowid)
            connexion.cursor.execute("INSERT INTO recevoir_notification (idNotification, idUtilisateur, estVu) VALUES (?, ?, ?)", (notification.id, ajoutMembre.idUtilisateur, 0))
        choix = int(input("Voulez-vous ajouter un membre? (1 = oui/ autres chiffres = non)\n"))
    print("\nGroupe créé avec succès\n")
    input("Appuyer sur entrer pour continuer ...")
    utilisateur.userGroups(user)

def isAllreadyAMember(userId, groupId):
    res = connexion.cursor.execute("SELECT * FROM appartenance WHERE idUtilisateur = ? AND idGroupe = ?", (userId, groupId)).fetchone()
    return res is not None
