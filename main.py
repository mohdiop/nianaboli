import connexion, createUser, connectUser, models, creationGroupe, sys, utilisateur as u, notification, administrateur, style, os

connexion.initialize()

def authentification():
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives")
    choix = 109309
    while(choix not in (1, 2, 3, 0)):
        print("1.) Connexion\n2.) Inscription\n3.) Quitter\n")
        choix = int(input("Votre choix : "))

    user: models.UtilisateurInfo = None

    match choix:
        case 1:
            user = connectUser.login()
        case 2: 
            user = createUser.creationProcess()
        case 3:
            os.system('clear' if os.name == 'posix' else 'cls')
            style.showStyledTitleCyan("À bientôt!")
            sys.exit()
        case 0:
            administrateur.seConnecter()
    if(user is None):
        authentification()
    else:
        menuPrincipal(user)

def menuPrincipal(utilisateur: models.UtilisateurInfo):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan(f"Bienvenue {utilisateur.prenom} {utilisateur.nom}")
    print("\n1.) Créer un groupe\n2.) Visualiser mes groupes\n3.) Notifications\n4.) Se déconnecter\n")

    choix = int(input("Votre choix : "))

    match choix:
        case 1:
            creationGroupe.creationGroupe(utilisateur)
        case 2: 
            u.userGroups(utilisateur)
        case 3:
            notification.viewNotifications(utilisateur)
        case 4:
            utilisateur = None
            authentification()

if (__name__ == '__main__'):
    try:
        authentification() 
    except (ValueError, KeyboardInterrupt, EOFError) as e:
        os.system('clear' if os.name == 'posix' else 'cls')
        style.showStyledTitleCyan(f"La console s'est arrêtée, raison : {type(e)}")
        sys.exit()