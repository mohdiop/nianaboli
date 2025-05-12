import models
import createUser
import connexion
from datetime import datetime

def isAdministrateur(user_id, group_id):
    res = connexion.cursor.execute(
        "SELECT * FROM appartenance WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'",
        (user_id, group_id)
    ).fetchone()
    return res is not None

def isAlreadyAMember(user_id, group_id):
    res = connexion.cursor.execute(
        "SELECT * FROM appartenance WHERE idUtilisateur = ? AND idGroupe = ?",
        (user_id, group_id)
    ).fetchone()
    return res is not None

def getGroupeByNom(nom_groupe):
    nom_groupe = nom_groupe.lower().strip()
    res = connexion.cursor.execute(
        "SELECT * FROM groupe WHERE LOWER(nom) = ?",
        (nom_groupe,)
    ).fetchone()
    return res

def ajouterMembre(adminUser: models.UtilisateurInfo):
    print("\n---------- Ajout d’un membre dans un groupe existant ----------\n")

    groupe_data = None
    while groupe_data is None:
        nom_groupe = input("Nom du groupe : ").strip()
        groupe_data = getGroupeByNom(nom_groupe)
        if groupe_data is None:
            print(" Groupe introuvable. Veuillez réessayer.\n")

    id_groupe = groupe_data[0]

    while not isAdministrateur(adminUser.id, id_groupe):
        print("Vous n’êtes pas administrateur de ce groupe. Action interdite.")
        nom_groupe = input("Nom d’un groupe dont vous êtes administrateur : ").strip()
        groupe_data = getGroupeByNom(nom_groupe)
        if groupe_data is None:
            print(" Groupe introuvable. Veuillez réessayer.\n")
            continue
        id_groupe = groupe_data[0]

    membre = None
    while membre is None:
        telephone = input("Numéro du membre à ajouter : ").strip()
        membre = createUser.getUserByTel(telephone)
        if membre is None:
            print(" Utilisateur introuvable. Veuillez réessayer.")
        elif membre.telephone == adminUser.telephone:
            print(" Vous êtes déjà l’administrateur de ce groupe.")
            membre = None
        elif isAlreadyAMember(membre.id, id_groupe):
            print(" Ce membre fait déjà partie du groupe.")
            membre = None

    # Ajout du membre
    dateAjout = datetime.now().strftime("%d-%m-%Y à %H:%M:%S")
    connexion.cursor.execute(
        "INSERT INTO appartenance (idUtilisateur, idGroupe, dateAjout, role) VALUES (?, ?, ?, ?)",
        (membre.id, id_groupe, dateAjout, "MEMBRE")
    )
    print(f" {membre.prenom} {membre.nom} a bien été ajouté au groupe '{nom_groupe}'.")
