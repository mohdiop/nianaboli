import connexion, createUser, connectUser, models, creationgroupe

connexion.initialize()
print("------------- Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives -------------")

def authentification():
    choix = 0
    while(choix not in (1, 2)):
        choix = int(input("1.) Connexion\n2.) Inscription\n"))

    user = None

    if(choix == 1):
        user = connectUser.login()
    elif(choix == 2):
        user = createUser.creationProcess()
    menuPrincipal(user)

def menuPrincipal(utilisateur: models.UtilisateurInfo):
    print(f"\nBienvenue {utilisateur.prenom} {utilisateur.nom} :)\n")
    print("----------------------------------------------------------------------------")
    print("\n1.) Créer un groupe\n2.) Visualiser mes groupes\n3.) Se déconnecter\n")

    choix = int(input("Votre choix : "))

    if(choix == 1):
        creationgroupe.creationGroupe(utilisateur)
    elif(choix == 3):
        utilisateur = None
        authentification()

authentification()


connexion.con.close