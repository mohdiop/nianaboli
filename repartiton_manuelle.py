import connexion, models, os, style
from datetime import datetime

def repartiotionManuelle(depense: models.Depense, members: list, nomGroupe: str):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Répartition Manuelle")
    print("Montant à payer pour :")
    connexion.con.autocommit = False
    for member in members:
        montantAPayerPourMembre = int(input(f"- {member.utilisateur.prenom} {member.utilisateur.nom} : "))
        notification = models.Notification(
            f"Création de dépense dans le groupe {nomGroupe}",
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

