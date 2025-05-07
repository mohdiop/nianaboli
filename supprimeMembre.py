import connexion
import models

def supprimerMembreDuGroupe(nom, nom_groupe):
    # Trouver l'utilisateur
    utilisateur = connexion.con.execute(
        "SELECT id_utilisateur FROM Utilisateur WHERE nom = ?", (nom,)
    ).fetchone()

    if not utilisateur:
        print(f"Aucun utilisateur trouvé avec le nom : {nom}")
        return

    id_utilisateur = utilisateur[0]

    # Trouver le groupe
    groupe = connexion.con.execute(
        "SELECT id_groupe FROM Groupe WHERE nom_groupe = ?", (nom_groupe,)
    ).fetchone()

    if not groupe:
        print(f"Aucun groupe trouvé avec le nom : {nom_groupe}")
        return

    id_groupe = groupe[0]

    # Vérifier s'il est bien dans le groupe
    appartenance = connexion.con.execute(
        "SELECT * FROM Appartenance WHERE id_utilisateur = ? AND id_groupe = ?",
        (id_utilisateur, id_groupe)
    ).fetchone()

    if not appartenance:
        print(f"L'utilisateur '{nom}' n'appartient pas au groupe '{nom_groupe}'.")
        return

    # Supprimer la relation dans Appartenance
    connexion.con.execute(
        "DELETE FROM Appartenance WHERE id_utilisateur = ? AND id_groupe = ?",
        (id_utilisateur, id_groupe)
    )
    connexion.con.commit()

    
