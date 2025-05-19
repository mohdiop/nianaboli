import connexion, createUser
from datetime import datetime
from enum import Enum

class Utilisateur:
    def __init__(self, nom, prenom, telephone, motDePasse: str):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.motDePasse = motDePasse
    
    def creerCompte(self):
        values = (self.nom, self.prenom, self.telephone, self.motDePasse)
        connexion.con.execute("INSERT INTO utilisateur (nom, prenom, telephone, motDePasse) VALUES (?,?,?,?)", values)

    def setId(self, id):
        self.id = id

class UtilisateurInfo:
    def __init__(self, id, nom, prenom, telephone):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone

    def creerGroupe(self, nom):
        dateCreation = f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"
        values = (nom, dateCreation, self.id)
        connexion.cursor.execute("INSERT INTO groupe (nom, dateCreation, idUtilisateur) VALUES (?, ?, ?)", values)
        groupe = Groupe(
            nom,
            dateCreation,
            self.id
        )
        groupe.setId(connexion.cursor.lastrowid)
        
        values = (self.id, groupe.id, dateCreation, "ADMINISTRATEUR")
        connexion.cursor.execute("INSERT INTO appartenance (idUtilisateur, idGroupe, dateAjout, role) VALUES (?, ?, ?, ?)", values)
        return groupe

    def faireUnPaiement(self, idDepense, montant):
        values = (self.id, idDepense, montant, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0)
        connexion.con.execute("INSERT INTO paiement (idUtilisateur, idDepense, montant, date, estValide)", values)
    
    def historiqueDepenses(self):
        resources = connexion.con.execute("SELECT * FROM depense WHERE idUtilisateur = ?", (self.id,)).fetchall()
        depenses = []
        for res in resources: 
            depense = Depense(
                idGroupe=res[1],
                titre=res[2],
                description=res[3],
                dateCreation=res[4],
                montant=res[5]
            )
            depense.setId(res[0])
            depenses.append(depense)
        return depenses

class Groupe: 
    def __init__(self, nom, dateCreation, idUtilisateur):
        self.nom = nom
        self.dateCreation = dateCreation
        self.utilisateur = createUser.getUserById(idUtilisateur)

    def __lt__(self, other):
        return self.dateCreation < other.dateCreation
    
    def setId(self, id):
        self.id = id
    
    def modifierNom(self, nom):
        connexion.con.execute("UPDATE groupe SET nom = ? WHERE id = ?", (nom, self.id))

class Depense:
    def __init__(self, idGroupe, montant, titre, description,  dateCreation):
        self.idGroupe = idGroupe
        self.titre = titre
        self.montant = montant
        self.description = description
        self.dateCreation = dateCreation
        self.repartitions = []

    def setId(self, id):
        self.id = id
    
class Paiement:
    def __init__(self, montant, datePaiement, estValide):
        self.montant = montant
        datePaiement = datePaiement
        self.estValide = estValide
    
    def setId(self, id):
        self.id = id

class Administrateur:
    def __init__(self, nom, prenom, telephone, motDePasse):
        self.nom = nom
        self.prenom = prenom
        self.motDePasse = motDePasse
        self.telephone = telephone
    def setId(self, id):
        self.id = id

class Role(Enum): 
    ADMINISTRATEUR = 1
    MEMBRE = 2

class Appartenance:
    def __init__(self, idUtilisateur, idGroupe, dateAjout, role: Role):
        self.idUtilisateur = idUtilisateur
        self.idGroupe = idGroupe
        self.dateAjout = dateAjout
        self.role = role

class Participation: 
    def __init__(self, idUtilisateur, idDepense, montantAPayer):
        self.idUtilisateur = idUtilisateur
        self.idDepense = idDepense
        self.montantAPayer = montantAPayer

    def setId(self, id):
        self.id = id

class Notification: 
    def __init__(self, titre, contenu, date):
        self.titre = titre
        self.contenu = contenu
        self.date = date

    def setId(self, id):
        self.id = id

class RecevoirNotification:
    def __init__(self, idUtilisateur, idNotification):
        self.idUtilisateur = idUtilisateur
        self.idNotification = idNotification

class ChangementMotDePasse:
    def __init__(self, id, idAdministrateur, idUtilisateur, dateModification):
        self.id  = id
        self.idAdministrateur = idAdministrateur
        self.idUtilisateur = idUtilisateur
        self.dateModification = dateModification