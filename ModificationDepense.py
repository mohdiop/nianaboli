def modifier_depense(id_utilisateur, id_groupe):
    from connexion import connexion
    cursor = connexion.cursor()

    # Vérification que l'utilisateur est administrateur
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_utilisateur, id_groupe))

    if not cursor.fetchone():
        print(" Seuls les administrateurs peuvent modifier une dépense.")
        return

    # Demander le titre de la dépense
    titre = input("Titre de la dépense à modifier : ").strip()

    # Rechercher les dépenses correspondant
    cursor.execute("""
        SELECT id, titre, description, montant, date FROM depense
        WHERE titre = ? AND idGroupe = ?
    """, (titre, id_groupe))

    depenses = cursor.fetchall()

    if not depenses:
        print(" Aucune dépense trouvée avec ce titre.")
        return

    # S'il y a plusieurs depense du même titre, l'utilisateur doit choisir laquelle il compte modifier
    if len(depenses) > 1:
        print("\nPlusieurs dépenses trouvées :")
        for i, d in enumerate(depenses, start=1):
            print(f"{i}. ID: {d[0]} | Montant: {d[3]}€ | Date: {d[4]} | Description: {d[2]}")

        try:
            choix = int(input("Numéro de la dépense à modifier : "))
            id_depense = depenses[choix - 1][0]
        except (ValueError, IndexError):
            print(" Choix invalide.")
            return
    else:
        id_depense = depenses[0][0]

    # Afficher les champs modifiables
    print("\nChamps modifiables : titre, description, montant")
    champs = input("Quels champs voulez-vous modifier ? (séparés par des virgules, ex : titre,montant) : ").strip().lower()
    champs = [ch.strip() for ch in champs.split(",")]

    # Préparer les parties de la requête
    valeurs = []
    set_clauses = []

    if "titre" in champs:
        nouveau_titre = input("Nouveau titre : ").strip()
        set_clauses.append("titre = ?")
        valeurs.append(nouveau_titre)

    if "description" in champs:
        nouvelle_description = input("Nouvelle description : ").strip()
        set_clauses.append("description = ?")
        valeurs.append(nouvelle_description)

    if "montant" in champs:
        try:
            nouveau_montant = int(input("Nouveau montant  : "))
            set_clauses.append("montant = ?")
            valeurs.append(nouveau_montant)
        except ValueError:
            print(" Montant invalide.")
            return

    if not set_clauses:
        print(" Aucun champ reconnu à modifier.")
        return

    # Construire et exécuter la requête SQL
    sql = f"UPDATE depense SET {', '.join(set_clauses)} WHERE id = ?"
    valeurs.append(id_depense)

    try:
        cursor.execute(sql, tuple(valeurs))
        connexion.commit()
        print(" Dépense mise à jour avec succès.")
    except Exception as e:
        print(f" Erreur lors de la mise à jour : {e}")