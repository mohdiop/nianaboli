import connexion, models, createUser

def viewStatisque():
    print("\n\n--------- Statistiques ---------\n\n")
    print("--------- Les groupes crées ---------\n")
    viewAllGroups()

def viewAllGroups(): 
    groupes = getAllGroups()
    for groupe in groupes:
        proprietaire = createUser.getUserById(groupe.utilisateur.id)
        membres = getMembersByGroupId(groupe.id)
        print("----------------------------------------------------------------------------")
        print(groupes.index(groupe)+1)
        print(f"Nom du groupe : {groupe.nom}")
        print(f"Créé par      : {proprietaire.prenom} {proprietaire.nom}")
        print(f"Le            : {groupe.dateCreation}")
        print(f"\nLes membres du groupe {groupes.index(groupe)+1}\n")
        for membre in membres: 
            print(f"| Nom : {membre.utilisateur.prenom} {membre.utilisateur.nom} Tel : {membre.utilisateur.telephone} ajouté le {membre.dateAjout}")
    print("----------------------------------------------------------------------------")

class UtilisateurInfoGroupe:
    def __init__(self, utilisateur: models.UtilisateurInfo, dateAjout):
        self.utilisateur = utilisateur
        self.dateAjout = dateAjout

def getMembersByGroupId(idGroup):
    resources = connexion.cursor.execute("SELECT id, nom, prenom, telephone, appartenance.dateAjout FROM utilisateur INNER JOIN appartenance ON utilisateur.id = appartenance.idUtilisateur WHERE appartenance.idGroupe = ? AND role = 'MEMBRE'", (idGroup,))
    membres = []
    for resource in resources:
        membre = UtilisateurInfoGroupe(
            models.UtilisateurInfo(
                resource[0],
                resource[1],
                resource[2],
                resource[3]
            ),
            resource[4]
        )
        membres.append(membre)
    return membres

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

def getUserGroupsByUserId(userId):
    resources = connexion.cursor.execute("SELECT * FROM groupe INNER JOIN appartenance ON groupe.id = appartenance.idGroupe WHERE appartenance.idUtilisateur = ? AND appartenance.role = 'ADMINISTRATEUR'", (userId,)).fetchall()
    if(resources is None): return None
    groupes = []
    for resource in resources:
        groupe = models.Groupe(
            nom=resource[1],
            dateCreation=resource[2],
            idUtilisateur=resource[3]
        )
        groupe.setId(resource[0])
        groupes.append(groupe)
    return groupes

def getRelatedGroups(userId):
    resources = connexion.cursor.execute("SELECT * FROM groupe INNER JOIN appartenance ON groupe.id = appartenance.idGroupe WHERE appartenance.idUtilisateur = ? AND appartenance.role = 'MEMBRE'", (userId,)).fetchall()
    if(resources is None): return None
    groupes = []
    for resource in resources:
        groupe = models.Groupe(
            nom=resource[1],
            dateCreation=resource[2],
            idUtilisateur=resource[3]
        )
        groupe.setId(resource[0])
        groupes.append(groupe)
    return groupes

def viewMyGroups(user):
    groupes = getUserGroupsByUserId(user.id)
    if(groupes is None or groupes == []):
        print("\nVous n'avez créé aucun groupe\n")
    else:
        print("------------------------------ Mes Groupes ---------------------------------")
        print("----------------------------------------------------------------------------")
        for groupe in groupes:
            print(f"\nNom du groupe  : {groupe.nom}")
            print(f"\nCréé le        : {groupe.dateCreation}\n")
        print("----------------------------------------------------------------------------")
    choix = int(input("1.) Visualiser un groupe en particulier\n2.) Retour\n\nVotre choix : "))
    if(choix == 2):
        userGroups(user)
    else:
        print("Choisissez le groupe à visualiser\n")

def viewRelatedGroups(user):
    groupes = getRelatedGroups(user.id)
    if(groupes is None or groupes == []):
        print("\nVous ne faites partie d'aucun groupe\n")
    else:
        print("----------------------- Groupes dans lesquels je suis ----------------------")
        print("----------------------------------------------------------------------------")
        for groupe in groupes:
            adminGroupe = createUser.getUserById(groupe.utilisateur.id)
            print(f"\nNom du groupe  : {groupe.nom}")
            print(f"\nCréé le        : {groupe.dateCreation}")
            print(f"\nAdministrateur : {adminGroupe.prenom} {adminGroupe.nom}\n")
        print("----------------------------------------------------------------------------")
    userGroups(user)

def userGroups(user: models.UtilisateurInfo):
    print("\n1.) Mes groupes créés\n2.) Ceux dans lesquels je suis membre\n3.) Retour\n")
    choix = int(input("Votre choix : "))
    
    match choix:
        case 1:
            viewMyGroups(user)
        case 2: 
            viewRelatedGroups(user)
        case 3:
            import main
            main.menuPrincipal(user)
    