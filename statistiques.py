import connexion, models, createUser

def viewStatisque():
    print("\n\n--------- Statistiques ---------\n\n")
    print("--------- Les groupes crées ---------\n")
    viewAllGroups()

def viewAllGroups(): 
    groupes = getAllGroups()
    for groupe in groupes:
        proprietaire = createUser.getUserById(groupe.utilisateur.id)
        print("----------------------------------------------------------------------------")
        print("Nom du groupe : ", groupe.nom)
        print("Créé par      : ", proprietaire.prenom, proprietaire.nom)
        print("Le            : ", groupe.dateCreation)
    print("----------------------------------------------------------------------------")


def getAllGroups():
    resources = connexion.con.execute("SELECT * FROM groupe").fetchall()
    groupes = []
    for resource in resources:
        groupe = models.Groupe(
            nom=resource[1],
            dateCreation=resource[2],
            idUtilisateur=resource[3]
        )
        groupe.setId(resource[0])
        groupes.append(groupe)
    groupes.sort()
    return groupes
