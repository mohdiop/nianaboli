import connexion, createUser, connectUser, models, creationgroupe, sys, utilisateur as u, notification

connexion.initialize()

def authentification():
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\n\n------------- Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives -------------\n\n")
    choix = 0
    while(choix not in (1, 2, 3, 4)):
        print("1.) Connexion\n2.) Inscription\n3.) Quitter\n")
        choix = int(input("Votre choix : "))

    user: models.UtilisateurInfo = None

    match choix:
        case 1:
            user = connectUser.login()
        case 2: 
            user = createUser.creationProcess()
        case 3:
            sys.exit("À bientôt!")
    if(user is None):
        authentification()
    else:
        menuPrincipal(user)

def menuPrincipal(utilisateur: models.UtilisateurInfo):
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\nBienvenue {utilisateur.prenom} {utilisateur.nom} :)\n")
    print("----------------------------------------------------------------------------")
    print("\n1.) Créer un groupe\n2.) Visualiser mes groupes\n3.) Notifications\n4.) Se déconnecter\n")

    choix = int(input("Votre choix : "))

    match choix:
        case 1:
            creationgroupe.creationGroupe(utilisateur)
        case 2: 
            u.userGroups(utilisateur)
        case 3:
            notification.viewNotifications(utilisateur)
        case 4:
            utilisateur = None
            authentification()

if (__name__ == '__main__'):
    authentification() 