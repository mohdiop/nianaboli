import connexion, createUser, connectUser, models, creationgroupe, sys, administrateur, notification

connexion.initialize()

def authentification():
    print("\n\n------------- Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives -------------\n\n")
    choix = 0
    while(choix not in (1, 2, 3)):
        print("1.) Connexion\n2.) Inscription\n3.) Quitter\n")
        choix = int(input("Votre choix : "))

    user = None

    if(choix == 1):
        user = connectUser.login()
    elif(choix == 2):
        user = createUser.creationProcess()
    elif(choix == 3):
        sys.exit("À bientôt!")
    menuPrincipal(user)

def menuPrincipal(utilisateur: models.UtilisateurInfo):
    print(f"\nBienvenue {utilisateur.prenom} {utilisateur.nom} :)\n")
    print("----------------------------------------------------------------------------")
    print("\n1.) Créer un groupe\n2.) Visualiser mes groupes\n3.) Notifications\n4.) Se déconnecter\n")

    choix = int(input("Votre choix : "))

    if(choix == 1):
        creationgroupe.creationGroupe(utilisateur)
    elif(choix == 2): 
        administrateur.userGroups(utilisateur)
    elif(choix == 3):
        notification.viewNotifications(utilisateur)
    elif(choix == 4):
        utilisateur = None
        authentification()

if (__name__ == '__main__'):
    authentification() 

connexion.con.close()