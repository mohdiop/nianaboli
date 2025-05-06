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
        "SELECT id FROM groupe WHERE LOWER(nom) = LOWER(?)", (nom,)
    ).fetchone()
    return result[0] if result else None

def utilisateur_deja_dans_groupe(id_utilisateur, id_groupe):
    result = connexion.con.execute(
        "SELECT 1 FROM appartenance WHERE idUtilisateur = ? AND idGroupe = ?",
        (id_utilisateur, id_groupe)
    ).fetchone()
    return result is not None

def ajoutProcessus(choix):
    if choix == "a":
        print("\nAjout d'un membre à un groupe\n")
        telephoneUtilisateur = input("Entrez le numéro de telephone de l'utilisateur à ajouter : ")
        idUtilisateur = get_id_utilisateur(telephoneUtilisateur)
        if idUtilisateur is None:
            print("Utilisateur introuvable avec ce numero.")
            return
        
        nomGroupe = input("Entrez le nom du groupe : ")
        idGroupe = get_id_groupe(nomGroupe)
        if idGroupe is None:
            print("Groupe introuvable avec ce nom.")
            return
        
        if utilisateur_deja_dans_groupe(idUtilisateur, idGroupe):
         print("Cet utilisateur est déjà membre de ce groupe.")
         return
        
        role = input("Entrez le rôle (MEMBRE ou ADMINISTRATEUR) : ").upper()
        while role not in ["MEMBRE", "ADMINISTRATEUR"]:
            print("Rôle invalide. Veuillez entrer 'MEMBRE' ou 'ADMINISTRATEUR'.")
            role = input("Entrez le rôle (MEMBRE ou ADMINISTRATEUR) : ").upper()

        appartenance = models.Appartenance(idUtilisateur, idGroupe, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), role)
        appartenance.ajoutMembre()
        print("Membre ajouté avec succès au groupe.")