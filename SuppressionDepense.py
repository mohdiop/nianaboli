def supprimer_depense_par_titre(id_utilisateur, id_groupe):
    import connexion  # Connexion SQLite3
    cursor = connexion.cursor

    # Étape 1 : Vérifier que l'utilisateur est administrateur du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_utilisateur, id_groupe))

    if not cursor.fetchone():
        print("Seuls les administrateurs peuvent supprimer une dépense.")
        return

    # Étape 2 : Demander le titre de la dépense
    titre = input("Titre de la dépense à supprimer : ").strip()

    # Étape 3 : Rechercher toutes les dépenses avec ce titre dans ce groupe
    cursor.execute("""
        SELECT id, titre, description, dateCreation, montant FROM depense
        WHERE titre = ? AND idGroupe = ?
    """, (titre, id_groupe))

    depenses = cursor.fetchall()

    if not depenses:
        print(" Aucune dépense trouvée avec ce titre dans ce groupe.")
        return

    # Étape 4 : Si plusieurs dépenses ont le même titre, laisser l'utilisateur choisir
    if len(depenses) > 1:
        print("\nPlusieurs dépenses trouvées avec ce titre :")
        for i, dep in enumerate(depenses, start=1):
            print(f"{i}. ID: {dep[0]} | Montant: {dep[4]} | Date: {dep[3]} | Description: {dep[2]}")

        try:
            choix = int(input("Numéro de la dépense à supprimer : "))
            id_depense = depenses[choix - 1][0]
        except (ValueError, IndexError):
            print(" Choix invalide.")
            return
    else:
        id_depense = depenses[0][0]

    # Étape 5 : Demander confirmation avant suppression
    confirmation = input(f" Êtes-vous sûr de vouloir supprimer la dépense '{titre}' (ID {id_depense}) ? (oui/non) : ").strip().lower()
    if confirmation != 'oui':
        print(" Suppression annulée.")
        return

    # Étape 6 : Suppression dans l'ordre (paiement → participation → depense)
    try:
        cursor.execute("DELETE FROM paiement WHERE idDepense = ?", (id_depense,))
        cursor.execute("DELETE FROM participation WHERE idDepense = ?", (id_depense,))
        cursor.execute("DELETE FROM depense WHERE id = ?", (id_depense,))
        connexion.con.commit()
        print(f" Dépense supprimée avec succès.")
    except Exception as e:
        print(f" Erreur lors de la suppression : {e}")
        



