import connexion  # Connexion SQLite3
cursor = connexion.cursor
def valid_paiement(id_utilisateur, id_groupe):

# Vérifier que l'utilisateur est administrateur du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_utilisateur, id_groupe))

    if not cursor.fetchone():
        print("Seuls les administrateurs peuvent valider un paiement.")
        return

    # Récupérer les paiements non validés
    cursor.execute("""
        SELECT paiement.id, paiement.montant, paiement.date,
            utilisateur.prenom, utilisateur.nom,
            depense.titre, depense.description
        FROM paiement
        INNER JOIN utilisateur ON utilisateur.id = paiement.idUtilisateur
        INNER JOIN depense ON depense.id = paiement.idDepense
        WHERE paiement.estValide = 0
    """)
    resultats = cursor.fetchall()

    if not resultats:
        print("Aucun paiement à valider.")
        return

    print("\n--- Liste des paiements à valider ---")
    for i, paiement in enumerate(resultats, start=1):
        print(f"\nPaiement n°{i}")
        print(f"Nom du redevable     : {paiement[4]}")
        print(f"Prénom du redevable  : {paiement[3]}")
        print(f"Montant payé         : {paiement[1]}")
        print(f"Date du paiement     : {paiement[2]}")
        print(f"Titre de la dépense  : {paiement[5]}")
        print(f"Description dépense  : {paiement[6]}")

    print("-------------------------------------")
    choix = input("Numéro du paiement à valider (ou '2' pour quitter) : ")

    if choix.lower() == '2':
        return

    try:
        choix_index = int(choix) - 1
        if choix_index < 0 or choix_index >= len(resultats):
            print("Numéro invalide.")
            return

        paiement_id = resultats[choix_index][0]

        cursor.execute("""
            UPDATE paiement
            SET estValide = 1
            WHERE id = ?
        """, (paiement_id,))
        print(" Paiement validé avec succès.")

    except ValueError:
        print("Entrée invalide.")
