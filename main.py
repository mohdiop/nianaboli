import connexion, createUser, connectUser

connexion.initialize()
print("------------- Bienvenue sur Nianaboli, votre console de gestion de dépenses collaboratives -------------")

choix = ""
while(choix not in ("c", "i")):
    choix = input("Entrer c pour Connexion ou i pour Inscription\n")

createUser.creationProcess(choix)
connectUser.login(choix)

connexion.con.close