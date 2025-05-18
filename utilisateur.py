import connexion, models, createUser, depense as dep, repartition_auto, repartiton_manuelle, addMembre, SuppressionDepense, paiement, os, style, historiquePaiement, validPaiement


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
    resources = connexion.cursor.execute("SELECT * FROM groupe WHERE idUtilisateur = ?", (userId,)).fetchall()
    if(not resources): return []
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
    if(not resources): return []
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
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Vos groupes créés")
    groupes = getUserGroupsByUserId(user.id)
    if(not groupes):
        print("\nVous n'avez créé aucun groupe\n")
        input("Appuyer sur entrer pour continuer ...")
        userGroups(user)
    else:
        indexes = [0,]
        for groupe in groupes:
            indexes.append(groupes.index(groupe) + 1)
            print(f"\nGroupe n°{groupes.index(groupe) + 1}")
            print(f"\nNom du groupe  : {groupe.nom}")
            print(f"\nCréé le        : {groupe.dateCreation}\n")
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

def viewGroup(groupe: models.Groupe, user: models.UtilisateurInfo):
    if(groupe.utilisateur.id == user.id):
        os.system('clear' if os.name == 'posix' else 'cls')
        style.showStyledTitleCyan(f"Groupe {groupe.nom} créé le {groupe.dateCreation} par vous")
    else:
        administrateur = createUser.getUserById(groupe.utilisateur.id)
        userName = administrateur.prenom + " " + administrateur.nom
        os.system('clear' if os.name == 'posix' else 'cls')
        style.showStyledTitleCyan(f"Groupe {groupe.nom} créé le {groupe.dateCreation} par {userName}")
    
    print("\n1.) Créer une dépense\n2.) Liste des dépenses\n3.) Ajouter membre\n4.) Liste des membres\n5.) Retour")
    choix = int(input("Votre choix : "))
    while(choix not in (1, 2, 3, 4, 5)):
        print("Choix invalide!")
        choix = int(input("Votre choix : "))
    
    if(choix == 1):
        depense = dep.creation_depense(user.id, groupe.id)
        if(type(depense) is not models.Depense):
            print(depense)
            input("Appuyer entrer pour continuer ...")
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
                resultat = repartition_auto.repartitionAuto(depense, members, groupe.nom)
                print(resultat)
            else:
                resultat = repartiton_manuelle.repartiotionManuelle(depense, members, groupe.nom)
                print(resultat)
            input("Appuyer entrer pour continuer ...")

    elif(choix == 2):
        viewExpenses(groupe, user)
    elif(choix == 3):
        addMembre.addMember(user, groupe)
        input("Appuyer sur entrée pour continuer ...")
        viewGroup(groupe, user)
    elif(choix == 4):
        os.system('clear' if os.name == 'posix' else 'cls')
        style.showStyledTitleCyan(f"Les membres du Groupe {groupe.nom}")
        membres = getMembersByGroupId(groupe.id)
        admin = UtilisateurInfoGroupe(
            createUser.getUserById(groupe.utilisateur.id),
            groupe.dateCreation
        )
        admin.role = "ADMINISTRATEUR"
        membres.append(admin)
        for membre in membres:
            print(f"{membre.utilisateur.prenom} {membre.utilisateur.nom} -- Rôle : {membre.role}\n")
        input("Appuyer sur entrer pour continuer ...")
        viewGroup(groupe, user)
    elif(choix == 5):
        viewMyGroups(user)


def viewExpenses(groupe: models.Groupe, user: models.UtilisateurInfo):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan(f"Dépenses Groupe {groupe.nom}")
    depenses = getAllExpensesByGroupId(groupe.id)
    if(not depenses):
        print("\nAucune dépense pour ce groupe\n")
        input("Appuyer entrer pour continuer ...")
        viewGroup(groupe, user)
    else:
        indexes = []
        for depense in depenses:
            index = depenses.index(depense)
            indexes.append(index+1)
            print(f"Dépense n°       : {index+1}")
            showExpense(depense)
            print("----------------------------------------------------------------------------")
        print("\n1.) Voir une dépense en particulier\n2.) Supprimer une dépense\n3.) Retour\n")
        choix = int(input("Votre choix : "))
        while(choix not in (1, 2, 3)):
            print("Choix invalide!")
            choix = int(input("Votre choix : "))
        
        match choix:
            case 1:
                choix = int(input("Numéro de la dépense : "))
                while(choix not in indexes):
                    print("Numéro invalide veuillez fournir un numéro valide!")
                    choix = int(input("Numéro de la dépense : "))
                viewExpense(depenses[choix-1], groupe, user)
            case 2:
                SuppressionDepense.supprimer_depense_par_titre(user.id, groupe.id)
                input("Appuer entrer pour continuer ...")
                viewGroup(groupe, user)
            case 3:
                viewGroup(groupe, user)

def showExpense(depense: models.Depense):
    print(f"Titre            : {depense.titre}")
    print(f"Description      : {depense.description}")
    print(f"Date de création : {depense.dateCreation}")
    print(f"Montant          : {depense.montant} FCFA\n")

def viewExpense(depense: models.Depense, groupe: models.Groupe, user: models.UtilisateurInfo):
    os.system('clear' if os.name == 'posix' else 'cls')
    paiements = getCurrentPaiementStatus(depense)
    style.showStyledTitleCyan(f"Dépense : {depense.titre} créée le : {depense.dateCreation}")
    style.showStyledTitleReset(f"Montant total à payer : {depense.montant} FCFA")
    style.showStyledTitleGreen(f"Montant total payé    : {paiements} FCFA")
    style.showStyledTitleYellow(f"Montant restant       : {depense.montant - paiements} FCFA")
    print("1.) Voir les paiements\n2.) Faire un paiement\n3.) Valider un paiement\n4.) Retour")
    choix = int(input("Votre choix : "))
    match choix:
        case 1:
            historiquePaiement.listPaie(depense.id, depense.idGroupe)
            input("Appuyer entrer pour continuer ...")
            viewExpense(depense, groupe, user)
        case 2:
            paiement.effectuer_paiement(user, groupe, depense)
            input("Appuyer sur entrer pour continuer ...")
            viewExpense(depense, groupe, user)
        case 3:
            validPaiement.valid_paiement(user.id, groupe.id, depense.id)
            input("Appuyer entrer pour continuer ...")
            viewExpense(depense, groupe, user)
        case 4:
            viewExpenses(groupe, user)

def getCurrentPaiementStatus(depense: models.Depense):
    resource = connexion.cursor.execute("SELECT SUM(montant) FROM paiement WHERE idDepense = ?", (depense.id,)).fetchone()
    if resource[0] is None: return 0
    else: return resource[0]


def getAllExpensesByGroupId(idGroup: int):
    resources = connexion.cursor.execute("SELECT * FROM depense WHERE idGroupe = ?", (idGroup,)).fetchall()
    if(not resources): return []
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
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Groupes dans lesquels vous êtes membres")
    groupes = getRelatedGroups(user.id)
    if(not groupes):
        print("\nVous ne faites partie d'aucun groupe\n")
        input("Appuyer entrer pour continuer ...")
    else:
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
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("GROUPES")
    print("\n1.) Mes groupes créés\n2.) Ceux dans lesquels je suis membre\n3.) Retour\n")
    choix = int(input("Votre choix : "))
    while(choix not in (1, 2, 3)):
        print("Choix invalide!")
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
    