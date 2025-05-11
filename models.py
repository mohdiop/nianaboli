import connexion, createUser
from datetime import date
from enum import Enum

class Utilisateur:
    def __init__(self, nom, prenom, telephone, motDePasse):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.motDePasse = motDePasse
    
    def creerCompte(self):
        values = (self.nom, self.prenom, self.telephone, self.motDePasse)
        connexion.con.execute("INSERT INTO utilisateur (nom, prenom, telephone, motDePasse) VALUES (?,?,?,?)", values)

    def setId(self, id):
        self.id = id

    def creerGroupe(self, nom):
        values = (nom, date.today().strftime('%d/%m/%Y'), self.id)
        connexion.con.execute("INSERT INTO groupe (nom, dateCreation, idUtilisateur) VALUES (?, ?, ?)", values)

    def faireUnPaiement(self, idDepense, montant):
        values = (self.id, idDepense, montant, date.today().strftime('%d/%m/%Y'), 0)
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

class UtilisateurInfo:
    def __init__(self, id, nom, prenom, telephone):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone

class Groupe: 
    def __init__(self, nom, dateCreation, idUtilisateur=None):
        self.nom = nom
        self.dateCreation = dateCreation
        self.utilisateur = None

        if idUtilisateur is not None:
            self.utilisateur = createUser.getUserById(idUtilisateur)

    def setId(self, id):
        self.id = id
    
    def creerGroupe(self):
        if self.utilisateur is None:
            raise ValueError("Utilisateur non défini pour la création du groupe.")
        values = (self.nom, self.dateCreation, self.utilisateur.id)
        connexion.con.execute("INSERT INTO groupe (nom, dateCreation, idUtilisateur) VALUES (?, ?, ?)", values)

    def modifierNom(self, nom):
        connexion.con.execute("UPDATE groupe SET nom = ? WHERE id = ?", (nom, self.id))

import connexion

class Depense:
    repartition = []

    def __init__(self, idGroupe, montant, titre, description, dateCreation):
        self.idGroupe = idGroupe
        self.montant = montant
        self.titre = titre
        self.description = description
        self.dateCreation = dateCreation

    def setId(self, id):
        self.id = id

    def enregistrer(self):
        connexion.con.execute(
            "INSERT INTO depense (idGroupe, titre, description, dateCreation, montant) VALUES (?, ?, ?, ?, ?)",
            (self.idGroupe, self.titre, self.description, self.dateCreation, self.montant)
        )
        self.id = connexion.con.execute("SELECT last_insert_rowid()").fetchone()[0]
        connexion.con.commit()

    def repartir_manuellement(self, repartition_dict):
        for id_utilisateur, montant in repartition_dict.items():
            connexion.con.execute(
                "INSERT INTO participation (idUtilisateur, idDepense, montantAPaye) VALUES (?, ?, ?)",
                (id_utilisateur, self.id, montant)
            )
        connexion.con.commit()
    def repartir_automatiquement(self):
        utilisateurs = connexion.con.execute(
            "SELECT idUtilisateur FROM appartenance WHERE idGroupe = ?",
            (self.idGroupe,)
        ).fetchall()

        if not utilisateurs:
            print("Aucun utilisateur trouvé pour ce groupe.")
            return

        montant_par_utilisateur = self.montant // len(utilisateurs)
        reste = self.montant % len(utilisateurs)

        # Répartition du montant
        for (idUtilisateur,) in utilisateurs:
            connexion.con.execute(
                "INSERT INTO participation (idUtilisateur, idDepense, montantAPaye) VALUES (?, ?, ?)",
                (idUtilisateur, self.id, montant_par_utilisateur)
            )

        # Gestion du reste si nécessaire (cela peut être réparti ou stocké comme un solde)
        if reste > 0:
            print(f"Un reste de {reste} FCFA sera distribué.")
            # Tu peux ajouter une logique pour répartir le reste si nécessaire

        connexion.con.commit()
        print(f"Répartition automatique effectuée : {montant_par_utilisateur} FCFA par utilisateur.")



    
class Paiement:
    def __init__(self, montant, datePaiement, estValide):
        self.montant = montant
        datePaiement = datePaiement
        self.estValide = estValide
    
    def setId(self, id):
        self.id = id

class Administrateur:
    def __init__(self, nom, prenom, motDePasse, telephone):
        self.nom = nom
        self.prenom = prenom
        self.motDePasse = motDePasse
        self.telephone = telephone

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
    def __init__(self, titre, contenu):
        self.titre = titre
        self.contenu = contenu

    def setId(self, id):
        self.id = id

class RecevoirNotification:
    def __init__(self, idUtilisateur, idNotification, date):
        self.idUtilisateur = idUtilisateur
        self.idNotification = idNotification
        self.date = date