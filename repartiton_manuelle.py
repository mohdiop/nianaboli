import connexion, models, os, style, utilisateur
from datetime import datetime

class Repartition:
    def __init__(self, member, montant=0):
        self.member = member
        self.montant = montant
        

def repartiotionManuelle(depense: models.Depense, members: list, nomGroupe: str):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Répartition Manuelle")
    numberOfMember = len(members)
    montantTotal = depense.montant
    for member in members:
        if(montantTotal == 0):
            break
        montantAPayerPourMembre = 0
        if(numberOfMember == len(members)):
            print(f"\nMontant total de la dépense : {montantTotal}\nNombre d'utilisateurs : {numberOfMember}")
        else:
            print(f"\nMontant restant : {montantTotal}\nUtilisateur restant : {numberOfMember}")
        montantAPayerPourMembre = int(input(f"- {member.utilisateur.prenom} {member.utilisateur.nom} : "))
        while(montantAPayerPourMembre > montantTotal):
            print(f"Le montant ne peut pas dépasser {montantTotal}")
            montantAPayerPourMembre = int(input(f"- Veuillez réindiquer le montant pour {member.utilisateur.prenom} {member.utilisateur.nom} : "))
        while(numberOfMember is 1 and montantAPayerPourMembre < montantTotal):
            print(f"Tout le montant doit être réparti!")
            montantAPayerPourMembre = int(input(f"- Veuillez réindiquer le montant pour {member.utilisateur.prenom} {member.utilisateur.nom} : "))
        repartition = Repartition(
            member,
            montantAPayerPourMembre
        )
        depense.repartitions.append(repartition)
        montantTotal = montantTotal-montantAPayerPourMembre
        numberOfMember = numberOfMember-1
    if(numberOfMember is not 0):
        for i in range(len(depense.repartitions), len(members)):
            repartition = Repartition(
                members[i])
            depense.repartitions.append(repartition)

    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Validation de la répartition")
    for repartition in depense.repartitions:
        print(f"{repartition.member.utilisateur.prenom} {repartition.member.utilisateur.nom} va payer {repartition.montant} FCFA")
    print("1.) Valider répartition\n2.) Reprendre la répartition")
    choix = int(input("Votre choix : "))
    while(choix not in (1,2)):
        print("Choix invalide!")
        choix = int(input("Votre choix : "))
    match choix:
        case 1:
            connexion.con.autocommit = False
            for repartition in depense.repartitions:
                storeMember(repartition.member, nomGroupe, depense, repartition.montant)
            connexion.con.commit()
            connexion.con.autocommit = True
        case 2: 
            depense.repartitions = []
            repartiotionManuelle(depense, members, nomGroupe)
    return "Répartition effectuée avec succès"

def storeMember(member, nomGroupe, depense: models.Depense, montantAPayerPourMembre):
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

