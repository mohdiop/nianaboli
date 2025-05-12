import connexion, models, re, bcrypt

def creationProcess(): 
    print("Inscription\n")
    prenom = input("Votre prénom : ")
    while(prenom == ""):
        print("Le prénom ne peut pas être vide!")
        prenom = input("Votre prénom : ")
    nom = input("Votre nom : ")
    while(nom == ""):
        print("Le nom ne peut pas être vide!")
        nom = input("Votre nom : ")
    telephone = input("Votre telephone : ")
    while(getUserByTel(telephone) is not None or telephone == "" or not isValidPhone(telephone)):
        if(getUserByTel(telephone) is not None):
            print("Ce numéro de téléphone appartient à un utilisateur!")
        elif(telephone == ""):
            print("Le numéro de téléphone ne peut pas être vide!")
        else:
            print("Le numéro de téléphone est incorrect!")
        telephone = input("Votre numéro de téléphone : ")
    motDePasse = input("Votre mot de passe : ")
    while(not isValidPassword(motDePasse)):
        print("Le mot doit contenir au moins\n1 majuscule,\n1 caractère spécial,\n1 chiffre\net au moins 6 caractères en tout!")
        motDePasse = input("Votre mot de passe : ")
    utilisateur = models.Utilisateur(nom, prenom, telephone, bcrypt.hashpw(motDePasse.encode(), bcrypt.gensalt()))
    utilisateur.creerCompte()
    utilisateur = getUserByTel(telephone)
    user = models.UtilisateurInfo(
        utilisateur.id,
        utilisateur.nom,
        utilisateur.prenom,
        utilisateur.telephone
    )
    return user

def isValidPhone(telephone):
    return re.match("^[76589]\d{7}$", telephone)

def isValidPassword(motDePasse):
    return re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%^&*()-_+=<>?]).{6,}$", motDePasse)
   
def getUserByTel(telephone: str):
    utilisateurTrouve = connexion.con.execute("SELECT * FROM utilisateur WHERE telephone = ?", (telephone,)).fetchone()
    if (utilisateurTrouve is None) : return None
    utilisateur = models.Utilisateur(
        utilisateurTrouve[1],
        utilisateurTrouve[2],
        utilisateurTrouve[3],
        utilisateurTrouve[4]
    )
    utilisateur.setId(utilisateurTrouve[0])
    return utilisateur

def getUserById(id): 
    utilisateurTrouve = connexion.con.execute("SELECT * FROM utilisateur WHERE id = ?", (id,)).fetchone()
    utilisateur = models.UtilisateurInfo(
        utilisateurTrouve[0],
        utilisateurTrouve[1],
        utilisateurTrouve[2],
        utilisateurTrouve[3]
    )
    return utilisateur

def getAllUsers():
    users = connexion.con.execute("SELECT * FROM utilisateur").fetchall()
    utilisateurs = []
    for user in users: 
        utilisateur = models.Utilisateur(
            user[1],
            user[2],
            user[3],
            user[4]
        )
        utilisateur.setId(user[0])
        utilisateurs.append(utilisateur)
    return utilisateurs