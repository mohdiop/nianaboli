import connexion

class Utilisateur:
    def __init__(self, nom, prenom, email, motDePasse):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.motDePasse = motDePasse
    
    def creerCompte(self):
        values = (self.nom, self.prenom, self.email, self.motDePasse)
        connexion.con.execute("INSERT INTO utilisateur (nom, prenom, email, motDePasse) VALUES (?,?,?,?)", values)

def creationProcess(choix): 
    if (choix == "i"):
        print("Inscription\n")
        prenom = input("Votre prénom : ")
        nom = input("Votre nom : ")
        email = input("Votre email : ")
        motDePasse = input("Votre mot de passe : ")
        utilisateur = Utilisateur(nom, prenom, email, motDePasse)
        utilisateur.creerCompte()
        print("Votre compte a été créé avec succès!")
