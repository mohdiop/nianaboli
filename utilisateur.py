import connexion, models, createUser, Depense, repartition_auto, repartiton_manuelle, addMembre, SuppressionDepense, paiement


class UtilisateurInfoGroupe:
    def __init__(self, utilisateur: models.UtilisateurInfo, dateAjout):
        self.utilisateur = utilisateur
        self.dateAjout = dateAjout
        self.role = "MEMBRE"

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
        userGroups(user)
    else:
        print("------------------------------ Mes Groupes ---------------------------------")
        print("----------------------------------------------------------------------------")
        indexes = []
        for groupe in groupes:
            indexes.append(groupes.index(groupe) + 1)
            print(f"\nGroupe n°{groupes.index(groupe) + 1}")
            print(f"\nNom du groupe  : {groupe.nom}")
            print(f"\nCréé le        : {groupe.dateCreation}\n\n")
        print("----------------------------------------------------------------------------")
        choix = int(input("1.) Visualiser un groupe en particulier\n2.) Retour\n\nVotre choix : "))
        if(choix == 2):
            userGroups(user)
        else:
            print("Choisissez le numéro du groupe à visualiser\n")
            choix = int(input("Votre choix : "))
            while(choix not in indexes):
                print("Ce numéro ne figure pas dans les groupes affichés!")
                choix = int(input("Votre choix : "))
            viewGroup(groupes[choix-1], user)
            userGroups(user)

def viewGroup(groupe: models.Groupe, user: models.UtilisateurInfo):
    if(groupe.utilisateur.id == user.id):
        print(f"\nGroupe {groupe.nom} créé le {groupe.dateCreation} par moi")
    else:
        administrateur = createUser.getUserById(groupe.utilisateur.id)
        userName = administrateur.prenom + " " + administrateur.nom
        print(f"\nGroupe {groupe.nom} créé le {groupe.dateCreation} par {userName}")
    
    print("\n1.) Créer une dépense\n2.) Liste des dépenses\n3.) Ajouter membre\n4.) Liste des membres\n5.) Retour")
    choix = int(input("Votre choix : "))
    while(choix not in (1, 2, 3, 4, 5)):
        print("Choix invalide!")
        choix = int(input("Votre choix : "))
    
    if(choix == 1):
        depense = Depense.creation_depense(user.id, groupe.id)
        if(type(depense) is not models.Depense):
            print(depense)
            viewGroup(groupe, user)
        else:
            print("1.) Répartition automatique\n2.) Répartition manuelle")
            choix = int(input("Votre choix : "))
            while(choix not in (1, 2)):
                print("Choix invalide!")
                choix = int(input("Votre choix = "))
            members = getMembersByGroupId(groupe.id)
            members.append(UtilisateurInfoGroupe(groupe.utilisateur, ""))
            if(choix == 1):
                resultat = repartition_auto.repartitionAuto(depense, members)
                print(resultat)
            else:
                resultat = repartiton_manuelle.repartiotionManuelle(depense, members)
                print(resultat)
    elif(choix == 2):
        viewExpenses(groupe, user)
    elif(choix == 3):
        addMembre.addMember(user, groupe)
        viewGroup(groupe, user)
    elif(choix == 4):
        print(f"Les membres du Groupe {groupe.nom}\n")
        membres = getMembersByGroupId(groupe.id)
        admin = UtilisateurInfoGroupe(
            createUser.getUserById(groupe.utilisateur.id),
            groupe.dateCreation
        )
        admin.role = "ADMINISTRATEUR"
        membres.append(admin)
        for membre in membres:
            print(f"{membre.utilisateur.prenom} {membre.utilisateur.nom} -- Rôle : {membre.role}\n")
        viewGroup(groupe, user)
    elif(choix == 5):
        viewMyGroups(user)


def viewExpenses(groupe: models.Groupe, user: models.UtilisateurInfo):
    print(f"-------------------------- Dépenses Groupe {groupe.nom}----------------------------")
    depenses = getAllExpensesByGroupId(groupe.id)
    if(depenses is None):
        print("\nAucune dépense pour ce groupe\n")
    else:
        indexes = []
        for depense in depenses:
            index = depenses.index(depense)
            indexes.append(index+1)
            print(f"Dépense n°       : {index+1}")
            showExpense(depense)
    print("\n1.) Voir une dépense en particulier\n2.) Supprimer une dépense\n3.) Retour\n")
    choix = int(input("Votre choix : "))
    while(choix not in (1, 2, 3)):
        print("Choix invalide!")
        choix = int(input("Votre choix : "))
    
    match choix:
        case 1:
            print("Veuillez fournir le numéro de la dépense\n")
            choix = int(input("Votre choix : "))
            while(choix not in indexes):
                print("Numéro invalide veuillez fournir un numéro valide!")
                choix = int(input("Votre choix : "))
            viewExpense(depenses[choix-1], groupe, user)
        case 2:
            SuppressionDepense.supprimer_depense_par_titre(user.id, groupe.id)
            viewGroup(groupe, user)
        case 3:
            viewGroup(groupe, user)

def showExpense(depense: models.Depense):
    print(f"Titre            : {depense.titre}")
    print(f"Description      : {depense.description}")
    print(f"Date de création : {depense.dateCreation}")
    print(f"Montant          : {depense.montant} FCFA\n")

def viewExpense(depense: models.Depense, groupe: models.Groupe, user: models.UtilisateurInfo):
    showExpense(depense)
    print("1.) Voir les paiements\n2.) Faire un paiement\n3.) Retour")
    choix = int(input("Votre choix : "))
    match choix:
        case 1:
            pass
        case 2:
            paiement.effectuer_paiement(user, groupe, depense)
            viewExpenses(groupe, user)
        case 3:
            viewExpenses(groupe, user)


def getAllExpensesByGroupId(idGroup: int) -> list:
    resources = connexion.cursor.execute("SELECT * FROM depense WHERE idGroupe = ?", (idGroup,)).fetchall()
    if(resources is None):
        return None
    depenses = []
    for resource in resources:
        depense = models.Depense(
            idGroupe=resource[1],
            titre=resource[2],
            description=resource[3],
            dateCreation=resource[4],
            montant=resource[5]
        )
        depense.setId(resource[0])
        depenses.append(depense)
    return depenses


def viewRelatedGroups(user):
    groupes = getRelatedGroups(user.id)
    if(groupes is None or groupes is []):
        print("\nVous ne faites partie d'aucun groupe\n")
    else:
        print("----------------------- Groupes dans lesquels je suis ----------------------")
        print("----------------------------------------------------------------------------")
        indexes = [0,]
        for groupe in groupes:
            adminGroupe = createUser.getUserById(groupe.utilisateur.id)
            indexes.append(groupes.index(groupe) + 1)
            print(f"\nGroupe n°{groupes.index(groupe) + 1}")
            print(f"\nNom du groupe  : {groupe.nom}")
            print(f"\nCréé le        : {groupe.dateCreation}")
            print(f"\nAdministrateur : {adminGroupe.prenom} {adminGroupe.nom}\n")
        print("----------------------------------------------------------------------------")
        choix = int(input("Pour visualiser un groupe entrer son numéro ou 0 pour retourner : "))
        while(choix not in indexes):
            print("Choix invalide!")
            choix = int(input("Pour visualiser un groupe entrer son numéro ou 0 pour retourner : "))
        if(choix == 0):
            userGroups(user)
        else:
            viewGroup(groupes[choix-1], user)
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

def estAdmin(userId, groupeId):
    res = connexion.cursor.execute("SELECT * FROM appartenance WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'", (userId, groupeId)).fetchone()
    estAdmin = res is not None
    return estAdmin
    