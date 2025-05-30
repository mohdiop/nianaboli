import sqlite3, bcrypt


con = sqlite3.connect("nianaboli.db")
cursor = con.cursor()
con.autocommit = True 

def initialize():
    # Création de la table utilisateur
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "utilisateur (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, prenom TEXT NOT NULL, telephone TEXT UNIQUE NOT NULL, motDePasse TEXT NOT NULL)")

    # Création de la table groupe
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "groupe (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, dateCreation TEXT NOT NULL, idUtilisateur INTEGER NOT NULL, " \
    "FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id))")

    # Création de la table depense
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "depense (id INTEGER PRIMARY KEY AUTOINCREMENT, idGroupe INTEGER NOT NULL, titre TEXT NOT NULL, description TEXT NOT NULL, dateCreation TEXT NOT NULL, montant INTEGER NOT NULL, " \
    "FOREIGN KEY(idGroupe) REFERENCES groupe(id))")

    # Création de la table participation
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "participation (idUtilisateur INTEGER NOT NULL, idDepense INTEGER NOT NULL, montantAPayer INTEGER NOT NULL, " \
    "PRIMARY KEY(idUtilisateur, idDepense), FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id), FOREIGN KEY(idDepense) REFERENCES depense(id))")

    # Création de la table administrateur
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "administrateur (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, prenom TEXT NOT NULL, telephone TEXT NOT NULL, motDePasse TEXT NOT NULL)")

    #Ajout de l'administrateur par défaut au système
    if(not isAdminAllReadyCreated()):
        values = ("Diop", "Mohamed", "70313104", "$2a$12$U8Fwf.pJJP9iq4zbIVSLfe9Zgh.g819krPZQJE/BXk26GPLxa1yEm")
        con.execute("INSERT INTO administrateur (nom, prenom, telephone, motDePasse) VALUES (?, ?, ?, ?)", values)

    # Création de la table appartenance
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "appartenance (idUtilisateur INTEGER NOT NULL, idGroupe INTEGER NOT NULL, dateAjout TEXT NOT NULL, role TEXT CHECK(role IN ('ADMINISTRATEUR', 'MEMBRE')), " \
    "PRIMARY KEY(idUtilisateur, idGroupe), " \
    "FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id), FOREIGN KEY(idGroupe) REFERENCES groupe(id))")
    
    # Création de la table paiement
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "paiement (id INTEGER PRIMARY KEY AUTOINCREMENT, idUtilisateur INTEGER NOT NULL, idDepense INTEGER NOT NULL, montant INTEGER NOT NULL, date TEXT NOT NULL, estValide INTEGER CHECK(estValide IN (0,1)), " \
    "FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id), FOREIGN KEY(idDepense) REFERENCES depense(id))")

    # Création de la table notification
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "notification (id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT NOT NULL, contenu TEXT NOT NULL, date TEXT NOT NULL)")

    # Création de la table recevoir_notification
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "recevoir_notification (idNotification INTEGER NOT NULL, idUtilisateur INTEGER NOT NULL, estVu INTEGER CHECK(estVu IN (0,1)), " \
    "FOREIGN KEY(idNotification) REFERENCES notification(id), FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id), " \
    "PRIMARY KEY(idNotification, idUtilisateur))")

    # Création de la table changement_mot_de_passe
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "changement_mot_de_passe (id INTEGER PRIMARY KEY NOT NULL, idAdministrateur INTEGER NOT NULL, idUtilisateur INTEGER NOT NULL, dateModification TEXT NOT NULL, " \
    "FOREIGN KEY(idAdministrateur) REFERENCES administrateur(id), FOREIGN KEY(idUtilisateur) REFERENCES utilisateur(id))")

def isAdminAllReadyCreated() -> bool: 
    res = con.execute("SELECT * FROM administrateur WHERE telephone = '70313104' AND prenom = 'Mohamed' AND nom = 'Diop'").fetchone()
    if(res is not None): 
        return True
    else: 
        return False