def supprimer_groupe(connexion, id_utilisateur_demandeur, id_utilisateur_cible, id_groupe):
    cursor = connexion.cursor()

    # Vérifie que le demandeur est administrateur du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_utilisateur_demandeur, id_groupe))
    est_admin = cursor.fetchone()

    if not est_admin:
        return "Erreur : seul un administrateur peut supprimer un groupe."

    if id_utilisateur_demandeur == id_utilisateur_cible:
        return "Erreur : un administrateur ne peut pas se supprimer lui-même."

    # Vérifie que l'utilisateur ciblé fait partie du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ?
    """, (id_utilisateur_cible, id_groupe))
    est_membre = cursor.fetchone()

    if not est_membre:
        return "Erreur : l'utilisateur à supprimer du groupe n'existe pas."

    # Suppression de l'appartenance de l'utilisateur au groupe
    cursor.execute("""
        DELETE FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ?
    """, (id_utilisateur_cible, id_groupe))

    connexion.commit()
    return "Utilisateur supprimé du groupe avec succès."
