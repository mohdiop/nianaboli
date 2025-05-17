import connexion, models, bcrypt, createUser, utilisateur, main, style, os

def seConnecter():
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Connexion Admin")
    telephone = input("Votre numéro de téléphone: ")
    admin = getAdminByTel(telephone)
    while(admin is None):
        telephone = input("Compte administrateur introuvable! \nVérifiez votre numéro de téléphone: ")
        admin = getAdminByTel(telephone)

    motDePasse = input("Votre mot de passe: ")
    hashedMotDePasse = admin.motDePasse
    while(not bcrypt.checkpw(motDePasse.encode(), hashedMotDePasse.encode())):
        motDePasse = input(f"Mot de passe incorrect!\nVotre mot de passe: ")
    adminDashboard(admin)

def adminDashboard(admin: models.Administrateur):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle(f"Bienvenue sur votre Dashboard {admin.prenom} {admin.nom}")
    print("1.) Lister tous les groupes\n2.) Lister les utilisateurs\n3.) Changer le mot de passe d'un utilisateur\n4.) Se déconnecter\n")

    choix = int(input("Votre choix : "))
    while(choix not in (1, 2, 3, 4)):
        print("Choix invalide!\n")
        choix = int(input("Votre choix : "))

    match choix:
        case 1:
            voirGroupes()
        case 2:
            voirUtilisateurs()
        case 3:
            if(not getAllUtilisateurs()):
                print("\nAucun utilisateur dans le système\n")
                input("Appuyer entrer pour revenir au dashboard ...")
            else:
                changerMotDePasse()
        case 4:
            main.authentification()

    adminDashboard(admin)

def voirGroupes(): 
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Tous les groupes du système")
    groupes = getAllGroups()
    if (not groupes):
        print("\nAucun groupe dans le système\n")
    else:
        for groupe in groupes:
            proprietaire = createUser.getUserById(groupe.utilisateur.id)
            membres = utilisateur.getMembersByGroupId(groupe.id)
            print("----------------------------------------------------------------------------")
            print(groupes.index(groupe)+1)
            print(f"Nom du groupe : {groupe.nom}")
            print(f"Créé par      : {proprietaire.prenom} {proprietaire.nom}")
            print(f"Le            : {groupe.dateCreation}")
            print(f"\nLes membres du groupe {groupes.index(groupe)+1}\n")
            for membre in membres: 
                print(f"| Nom : {membre.utilisateur.prenom} {membre.utilisateur.nom} Tel : {membre.utilisateur.telephone} ajouté le {membre.dateAjout}")
        print("----------------------------------------------------------------------------")
    input("Appuyer entrer pour continuer ...")

def voirUtilisateurs():
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Tous les utilisateurs du système")
    utilisateurs = getAllUtilisateurs()
    if(not utilisateurs):
        print("\nAucun utilisateur dans le système\n")
    else:
        for utilisateur in utilisateurs:
            print("----------------------------------------------------------------------------")
            nombreGroupesCrees = getNumberOfCreatedGroupsByUserId(utilisateur.id)
            nombreGroupesAppartenance = getNumberOfRelatedGroupsByUserId(utilisateur.id)
            sommeDesPaiements = getAllPaymentByUserId(utilisateur.id)
            print(utilisateurs.index(utilisateur)+1)
            print(f"Nom Complet de l'utilisateur            : {utilisateur.prenom} {utilisateur.nom}")
            print(f"Numéro de téléphone                     : {utilisateur.telephone}")
            print(f"Nombre de groupes créés                 : {nombreGroupesCrees}")
            print(f"Nombre de groupes où il/elle est membre : {nombreGroupesAppartenance}")
            print(f"Total paiements effectués               : {sommeDesPaiements} FCFA")
        print("----------------------------------------------------------------------------")
    input("Appuyer sur entrer pour continuer ...")

def changerMotDePasse():
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Changement mot de passe utilisateur")
    telephone = input("Numéro de téléphone de l'utilisateur : ")
    utilisateur = createUser.getUserByTel(telephone)
    while(utilisateur is None):
        telephone = input("Utilisateur introuvable! \nRévérifiez le numéro de téléphone: ")
        utilisateur = createUser.getUserByTel(telephone)
    nouveauMotDePasse = input("Veuillez entrer le nouveau mot de passe : ")
    hashedPassword = bcrypt.hashpw(nouveauMotDePasse.encode(), bcrypt.gensalt())
    connexion.cursor.execute("UPDATE utilisateur SET motDePasse = ? WHERE id = ?", (hashedPassword, utilisateur.id))
    print("Mot de passe changé avec succès!")
    input("Appuyer sur entrer pour continuer ...")

def getAllUtilisateurs():
    resources = connexion.con.execute("SELECT * FROM utilisateur").fetchall()
    if not resources: return []
    utilisateurs = []
    for resource in resources:
        utilisateur = models.UtilisateurInfo(
            resource[0],
            resource[1],
            resource[2],
            resource[3]
        )
        utilisateurs.append(utilisateur)
    return utilisateurs

def getNumberOfCreatedGroupsByUserId(idUtilisateur: int) -> int:
    resource = connexion.cursor.execute("SELECT COUNT(*) FROM groupe where idUtilisateur = ?", (idUtilisateur,)).fetchone()
    if(resource[0] is None): 
        return 0
    else:
        return resource[0]

def getNumberOfRelatedGroupsByUserId(idUtilisateur: int) -> int:
    resource = connexion.cursor.execute("SELECT count(*) FROM appartenance where idUtilisateur = ? and role = 'MEMBRE'", (idUtilisateur,)).fetchone()
    if(resource[0] is None): 
        return 0
    else:
        return resource[0]

def getAllPaymentByUserId(idUtilisateur: int) -> int:
    resource = connexion.cursor.execute("SELECT SUM(montant) FROM paiement WHERE idUtilisateur = ?", (idUtilisateur,)).fetchone()
    if(resource[0] is None): 
        return 0
    else:
        return resource[0]

def getAllGroups():
    resources = connexion.con.execute("SELECT * FROM groupe").fetchall()
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
    groupes.sort()
    return groupes

def getAdminByTel(telephone: str):
    res = connexion.cursor.execute("SELECT * FROM administrateur WHERE telephone = ?", (telephone,)).fetchone()
    if(res is None): return None
    admin = models.Administrateur(
        res[1],
        res[2],
        res[3],
        res[4]
    )
    admin.setId(res[0])
    return admin