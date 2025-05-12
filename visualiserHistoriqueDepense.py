import connexion, models
def visualiser_historique_depenses(telephone):
    cursor = connexion.cursor

    # Récupérer le nom, prénom et id de l'utilisateur à partir du téléphone
    cursor.execute("""
        SELECT id, nom, prenom
        FROM utilisateur
        WHERE telephone = ?
    """, (telephone,))
    utilisateur = cursor.fetchone()

    if not utilisateur:
        print("Utilisateur non trouvé.")
        return

    id_utilisateur, nom, prenom = utilisateur

    # Requête pour récupérer les dépenses
    cursor.execute("""
        SELECT d.titre, d.description, d.montant, d.dateCreation, g.nom AS groupe, p.montantAPaye
        FROM participation p
        JOIN depense d ON p.idDepense = d.id
        JOIN groupe g ON d.idGroupe = g.id
        WHERE p.idUtilisateur = ?
        ORDER BY d.dateCreation DESC
    """, (id_utilisateur,))

    depenses = cursor.fetchall()

    if not depenses:
        print(f"Aucune dépense trouvée pour l'utilisateur {nom} {prenom}.")
        return

    print(f"\nHistorique des dépenses pour l'utilisateur {nom} {prenom} :\n")
    for dep in depenses:
        titre, description, montant, dateCreation, groupe, montantAPaye = dep
        print(f" Titre : {titre}")
        print(f"   Description : {description}")
        print(f"   Montant total : {montant} FCFA")
        print(f"   À payer par vous : {montantAPaye} FCFA")
        print(f"   Groupe : {groupe}")
        print(f"   Date : {dateCreation}\n")

