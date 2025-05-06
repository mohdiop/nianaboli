import connexion
import models
from datetime import datetime


def get_id_utilisateur(telephone):
    result = connexion.con.execute(
        "SELECT id FROM utilisateur WHERE telephone = ?", (telephone,)
    ).fetchone()
    return result[0] if result else None

def get_id_groupe(nom):
    result = connexion.con.execute(
        "SELECT id FROM groupe WHERE nom = ?", (nom,)
    ).fetchone()
    return result[0] if result else None

def ajoutProcessus(choix):
    if choix == "a":
        print("\nAjout d'un membre à un groupe\n")
        telephoneUtilisateur = input("Entrez le numéro de telephone de l'utilisateur à ajouter : ")
        nomGroupe = input("Entrez le nom du groupe : ")


        idUtilisateur = get_id_utilisateur(telephoneUtilisateur)
        idGroupe = get_id_groupe(nomGroupe)

        if idUtilisateur is None:
            print("Utilisateur introuvable avec ce numero.")
            return
        if idGroup is None:
            print("Groupe introuvable avec ce nom.")
            return

        participation = models.Appartenance(idUtilisateur, idGroupe, datetime.now(), "membre")
        participation.ajoutMembre()
        print("Membre ajouté avec succès au groupe.")