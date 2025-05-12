from datetime import datetime
import models, connexion

def repartitionAuto(depense: models.Depense, members: list):
    montantTotal = depense.montant
    montantAPayer = montantTotal // len(members)
    idDepense = depense.id
    notification = models.Notification(
        "Création Dépense",
        f"Vous contribuez désormais à la dépense {depense.titre}, votre montant à payer est : {montantAPayer} FCFA",
        f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"
    )
    values = (notification.titre, notification.contenu, notification.date)
    connexion.cursor.execute("INSERT INTO notification  (titre, contenu, date) VALUES (?, ?, ?)", values)
    notification.setId(connexion.cursor.lastrowid)

    for member in members:
        idUtilisateur = member.utilisateur.id
        values = (idUtilisateur, idDepense, montantAPayer)
        connexion.cursor.execute("INSERT INTO participation (idUtilisateur, idDepense, montantAPayer) VALUES (?, ?, ?)", values)

        values = (notification.id, idUtilisateur, 0)
        connexion.cursor.execute("INSERT INTO recevoir_notification (idNotification, idUtilisateur, estVu) VALUES (?, ?, ?)", values)

    return f"Répartition automatique effectuée, montant par membre : {montantAPayer} FCFA"

    
