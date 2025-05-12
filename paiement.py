import connexion
from datetime import datetime
import models

def effectuer_paiement(utilisateur: models.UtilisateurInfo):
    print("\n--- Effectuer un paiement ---")
    
    # Étape 1: Afficher les groupes de l'utilisateur
    groupes = get_user_groups(utilisateur.id)
    if not groupes:
        print("Vous n'êtes membre d'aucun groupe.")
        return
    
    print("\nVos groupes:")
    for i, groupe in enumerate(groupes, 1):
        print(f"{i}. {groupe.nom} (créé le {groupe.dateCreation})")
    
    # Étape 2: Sélectionner un groupe
    choix_groupe = int(input("\nChoisissez un groupe (numéro): ")) - 1
    if choix_groupe < 0 or choix_groupe >= len(groupes):
        print("Choix invalide.")
        return
    
    groupe_selectionne = groupes[choix_groupe]
    
    # Étape 3: Afficher les dépenses du groupe
    depenses = get_group_expenses(groupe_selectionne.id)
    if not depenses:
        print("Ce groupe n'a aucune dépense enregistrée.")
        return
    
    print(f"\nDépenses du groupe {groupe_selectionne.nom}:")
    for i, depense in enumerate(depenses, 1):
        print(f"{i}. {depense.titre} - {depense.montant} FCFA (le {depense.dateCreation})")
    
    # Étape 4: Sélectionner une dépense
    choix_depense = int(input("\nChoisissez une dépense (numéro): ")) - 1
    if choix_depense < 0 or choix_depense >= len(depenses):
        print("Choix invalide.")
        return
    
    depense_selectionnee = depenses[choix_depense]
    
    # Étape 5: Vérifier si l'utilisateur fait partie de la dépense
    participation = get_user_participation(utilisateur.id, depense_selectionnee.id)
    if not participation:
        print("Vous ne faites pas partie de cette dépense.")
        return
    
    montant_a_payer = participation.montantAPayer
    
    # Étape 6: Demander le montant à payer
    print(f"\nMontant à payer pour cette dépense: {montant_a_payer} FCFA")
    montant_paye = float(input("Entrez le montant que vous payez: "))
    
    if montant_paye < montant_a_payer:
        print(f"Attention: vous payez moins que le montant dû ({montant_a_payer} FCFA)")
    
    # Étape 7: Enregistrer le paiement
    enregistrer_paiement(utilisateur.id, depense_selectionnee.id, montant_paye)
    
    # Étape 8: Notifier l'administrateur
    notifier_administrateur(groupe_selectionne, utilisateur, depense_selectionnee, montant_paye)
    
    print("\nPaiement enregistré avec succès! Il sera validé par l'administrateur du groupe.")

def get_user_groups(user_id):
    """Récupère les groupes auxquels l'utilisateur appartient"""
    resources = connexion.con.execute(
        "SELECT groupe.id, groupe.nom, groupe.dateCreation, groupe.idUtilisateur "
        "FROM groupe INNER JOIN appartenance ON groupe.id = appartenance.idGroupe "
        "WHERE appartenance.idUtilisateur = ?", (user_id,)).fetchall()
    
    groupes = []
    for res in resources:
        groupe = models.Groupe(
            nom=res[1],
            dateCreation=res[2],
            idUtilisateur=res[3]
        )
        groupe.setId(res[0])
        groupes.append(groupe)
    return groupes

def get_group_expenses(group_id):
    """Récupère les dépenses d'un groupe"""
    resources = connexion.con.execute(
        "SELECT id, titre, description, dateCreation, montant "
        "FROM depense WHERE idGroupe = ?", (group_id,)).fetchall()
    
    depenses = []
    for res in resources:
        depense = models.Depense(
            idGroupe=group_id,
            titre=res[1],
            description=res[2],
            dateCreation=res[3],
            montant=res[4]
        )
        depense.setId(res[0])
        depenses.append(depense)
    return depenses

def get_user_participation(user_id, expense_id):
    """Vérifie si l'utilisateur participe à une dépense et retourne sa participation"""
    res = connexion.con.execute(
        "SELECT idUtilisateur, idDepense, montantAPaye "
        "FROM participation WHERE idUtilisateur = ? AND idDepense = ?", 
        (user_id, expense_id)).fetchone()
    
    if not res:
        return None
    
    return models.Participation(
        idUtilisateur=res[0],
        idDepense=res[1],
        montantAPayer=res[2]
    )

def enregistrer_paiement(user_id, expense_id, montant):
    """Enregistre un paiement dans la base de données"""
    date_paiement = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connexion.con.execute(
        "INSERT INTO paiement (idUtilisateur, idDepense, montant, date, estValide) "
        "VALUES (?, ?, ?, ?, ?)", 
        (user_id, expense_id, montant, date_paiement, 0))

def notifier_administrateur(groupe, utilisateur, depense, montant):
    """Envoie une notification à l'administrateur du groupe"""
    # Récupérer l'administrateur du groupe
    admin_id = groupe.utilisateur.id
    admin = models.UtilisateurInfo(admin_id, "", "", "")
    
    # Créer la notification
    titre = "Nouveau paiement à valider"
    contenu = (f"{utilisateur.prenom} {utilisateur.nom} a effectué un paiement de {montant} FCFA "
              f"pour la dépense '{depense.titre}' dans le groupe {groupe.nom}.")
    date_notif = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Enregistrer la notification
    connexion.con.execute(
        "INSERT INTO notification (titre, contenu, date) VALUES (?, ?, ?)",
        (titre, contenu, date_notif))
    
    notification_id = connexion.cursor.lastrowid
    
    # Lier la notification à l'administrateur
    connexion.con.execute(
        "INSERT INTO recevoir_notification (idNotification, idUtilisateur, estVu) "
        "VALUES (?, ?, ?)",
        (notification_id, admin_id, 0))