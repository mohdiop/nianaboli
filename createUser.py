import connexion
import models

def creationProcess(choix): 
    if (choix == "i"):
        print("Inscription\n")
        prenom = input("Votre prénom : ")
        nom = input("Votre nom : ")
        telephone = input("Votre telephone : ")
        motDePasse = input("Votre mot de passe : ")
        utilisateur = models.Utilisateur(nom, prenom, telephone, motDePasse)
        utilisateur.creerCompte()
        print("Votre compte a été créé avec succès!")
   
def getUserByTel(telephone: str):
    utilisateurTrouve = connexion.con.execute("SELECT * FROM utilisateur WHERE telephone = ?", (telephone,)).fetchone()
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
        utilisateurTrouve[1],
        utilisateurTrouve[2],
        utilisateurTrouve[3]
    )
    utilisateur.setId(utilisateurTrouve[0])
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