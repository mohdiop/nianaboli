import connexion, models
from datetime import datetime

def repartiotionManuelle(depense: models.Depense, members: list):
    print("Montant à payer pour :")
    connexion.con.autocommit = False
    for member in members:
        montantAPayerPourMembre = int(input(f"- {member.utilisateur.prenom} {member.utilisateur.nom} : "))
        notification = models.Notification(
            "Création Dépense",
            f"Vous contribuez désormais à la dépense {depense.titre}, votre montant à payer est : {montantAPayerPourMembre} FCFA",
            f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"
        )
        values = (notification.titre, notification.contenu, notification.date)
        connexion.cursor.execute("INSERT INTO notification  (titre, contenu, date) VALUES (?, ?, ?)", values)
        notification.setId(connexion.cursor.lastrowid)
        idUtilisateur = member.utilisateur.id
        values = (idUtilisateur, depense.id, montantAPayerPourMembre)
        connexion.cursor.execute("INSERT INTO participation (idUtilisateur, idDepense, montantAPayer) VALUES (?, ?, ?)", values)
        values = (notification.id, idUtilisateur, 0)
        connexion.cursor.execute("INSERT INTO recevoir_notification (idNotification, idUtilisateur, estVu) VALUES (?, ?, ?)", values)
        print(f"\nMontant restant : {depense.montant - montantAPayerPourMembre}\nUtilisateur restant : {len(members) - 1}")
    connexion.con.commit()
    connexion.con.autocommit = True
    return "Répartition effectuée avec succès"

