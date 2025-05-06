import connexion, createUser,ajoutMembre

connexion.initialize()
print("------------- Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives -------------")

choix = ""
while(choix not in ("c", "i","a")):
    choix = input("Entrer c pour Connexion ou i pour Inscription ou a pour ajouter un membre\n")

createUser.creationProcess(choix)
ajoutMembre.ajoutProcessus(choix)

connexion.con.close