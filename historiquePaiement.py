cursor = connexion.cursor
def listPaie():
    res= connexion.cursor.execute("""
        SELECT paiement.id, paiement.montant, paiement.date, paiement.estValide,
            utilisateur.prenom, utilisateur.nom,
            depense.titre, depense.description
        FROM paiement
        INNER JOIN utilisateur ON utilisateur.id = paiement.idUtilisateur
        INNER JOIN depense ON depense.id = paiement.idDepense
    """)
    res = cursor.fetchall()

    if not res:
        print("Aucun paiement pour le moment.")
        return

    print("\n--- Liste des paiements  ---")
    for i, paiement in enumerate(res, start=1):
        print(f"\nPaiement n°{i}")
        print(f"Nom du redevable     : {paiement[5]}")  # nom
        print(f"Prénom du redevable  : {paiement[4]}")  # prénom
        print(f"Montant payé         : {paiement[1]}")
        print(f"Date du paiement     : {paiement[2]}")
        print(f"Titre de la dépense  : {paiement[6]}")
        print(f"Description dépense  : {paiement[7]}")
        print(f"Statut               : {'Non validé' if paiement[3] == 0 else 'Validé'}")
