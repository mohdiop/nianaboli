import connexion
import models

def supprimerMembreDuGroupe(nom_utilisateur, nom_groupe):
    # Récupérer l'ID de l'utilisateur à partir de son nom
    utilisateur = connexion.con.execute(
        "SELECT id FROM Utilisateur WHERE nom = ?", (nom_utilisateur,)
    ).fetchone()

    if utilisateur is None:
        print("Utilisateur non trouvé.")
        return

    id_utilisateur = utilisateur[0]

    # Récupérer l'ID du groupe à partir de son nom
    groupe = connexion.con.execute(
        "SELECT id FROM Groupe WHERE nom = ?", (nom_groupe,)
    ).fetchone()

    if groupe is None:
        print("Groupe non trouvé.")
        return

    id_groupe = groupe[0]

    # Vérifier si l'utilisateur fait partie du groupe dans la table Appartenance
    appartenance = connexion.con.execute(
        "SELECT * FROM Appartenance WHERE id_utilisateur = ? AND id_groupe = ?",
        (id_utilisateur, id_groupe)
    ).fetchone()

    if appartenance is None:
        print("Ce membre ne fait pas partie de ce groupe.")
        return

    # Supprimer l'appartenance de cet utilisateur à ce groupe
    connexion.con.execute(
        "DELETE FROM Appartenance WHERE id_utilisateur = ? AND id_groupe = ?",
        (id_utilisateur, id_groupe)
    )
    connexion.con.commit()
    print(f" Le membre '{nom_utilisateur}' a été supprimé du groupe '{nom_groupe}'.")
if __name__ == "__main__":
    nom = input("Entrez le nom du membre à supprimer : ")
    nom_groupe = input("Entrez le nom du groupe : ")
    supprimerMembreDuGroupe(nom, nom_groupe)