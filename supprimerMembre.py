import connexion, models
def supprimer_membre( id_utilisateur_demandeur, id_utilisateur_cible, id_groupe):
    
    # Vérifie que le demandeur est administrateur du groupe
    cursor = connexion.cursor
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_utilisateur_demandeur, id_groupe))
    est_admin = cursor.fetchone()

    if not est_admin:
        return "Erreur : seul un administrateur peut supprimer un membre."

    if id_utilisateur_demandeur == id_utilisateur_cible:
        return "Erreur : un administrateur ne peut pas se supprimer lui-même."

    # Vérifie que le membre ciblé fait bien partie du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ?
    """, (id_utilisateur_cible, id_groupe))
    est_membre = cursor.fetchone()

    if not est_membre:
        return "Erreur : l'utilisateur à supprimer n'est pas membre de ce groupe."

    # Suppression
    cursor.execute("""
        DELETE FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ?
    """, (id_utilisateur_cible, id_groupe)) 

    return "Membre supprimé avec succès."
