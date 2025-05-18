import connexion, os, style
from datetime import datetime
import models

def effectuer_paiement(utilisateur: models.UtilisateurInfo, groupe: models.Groupe, depense: models.Depense):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Faire un paiement")
    
    depense_selectionnee = depense
    
    # Étape 5: Vérifier si l'utilisateur fait partie de la dépense
    participation = get_user_participation(utilisateur.id, depense_selectionnee.id)
    if not participation:
        print("Vous ne faites pas partie de cette dépense.")
        return
    
    montant_a_payer = participation.montantAPayer

    if(montant_a_payer == 0):
        print("Vous avez effectué tous vos paiements pour cette dépense!\n")
        return
    
    # Étape 6: Demander le montant à payer
    print(f"\nMontant à payer pour cette dépense: {montant_a_payer} FCFA")
    montant_paye = float(input("Entrez le montant que vous payez : "))
    
    if montant_paye < montant_a_payer:
        print(f"Attention: vous payez moins que le montant dû ({montant_a_payer} FCFA)")

    while(montant_a_payer < montant_paye):
        print("Impossible d'effectuer le paiement le montant payé est supérieur au montant à payer\n")
        montant_paye = float(input("Entrez le montant que vous payez: "))
    
    # Étape 7: Enregistrer le paiement
    enregistrer_paiement(utilisateur.id, depense_selectionnee.id, montant_paye)
    
    # Étape 8: Notifier l'administrateur
    notifier_administrateur(groupe, utilisateur, depense_selectionnee, montant_paye)
    
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Paiement effectué, il sera validé par l'administrateur")
def get_user_participation(user_id, expense_id):
    """Vérifie si l'utilisateur participe à une dépense et retourne sa participation"""
    res = connexion.con.execute(
        "SELECT idUtilisateur, idDepense, montantAPayer "
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
    connexion.con.autocommit = False
    """Enregistre un paiement dans la base de données"""
    date_paiement = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connexion.con.execute(
        "INSERT INTO paiement (idUtilisateur, idDepense, montant, date, estValide) "
        "VALUES (?, ?, ?, ?, ?)", 
        (user_id, expense_id, montant, date_paiement, 0))
    
    connexion.con.execute("UPDATE participation SET montantAPayer = montantAPayer - ? WHERE idUtilisateur = ? AND idDepense = ?",
                          (montant, user_id, expense_id))
    connexion.con.commit()
    connexion.con.autocommit = True

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
    connexion.cursor.execute(
        "INSERT INTO notification (titre, contenu, date) VALUES (?, ?, ?)",
        (titre, contenu, date_notif))
    
    notification_id = connexion.cursor.lastrowid
    
    # Lier la notification à l'administrateur
    connexion.cursor.execute(
        "INSERT INTO recevoir_notification (idNotification, idUtilisateur, estVu) "
        "VALUES (?, ?, ?)",
        (notification_id, admin_id, 0))