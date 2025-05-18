import connexion, style, os
import models
from datetime import datetime

def creation_depense(id_createur_depense, id_groupe):
    cursor = connexion.cursor

    # Vérifie que le demandeur est administrateur du groupe
    cursor.execute("""
        SELECT * FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_createur_depense, id_groupe))
    est_admin = cursor.fetchone() is not None

    if not est_admin:
        return " Seul un administrateur peut créer une dépense."

    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Création Dépense")
    titre = input("Titre de la dépense : ")
    description = input("Description de la dépense : ")
    
    try:
        montant = int(input("Montant de la dépense  : "))
    except ValueError:
        return " Le montant doit être un entier."

    date = f"{datetime.now().strftime("%d-%m-%Y")} à {datetime.now().strftime("%H:%M:%S")}"

    # Création de l'objet dépense (ajuste selon ta classe)
    depense = models.Depense(
        id_groupe,
        montant,
        titre,
        description,
        date
    )

    # Appel à la méthode pour insérer en BDD
    creerDepense(depense) # Assure-toi que cette méthode existe
    return depense

def creerDepense(depense: models.Depense):
    values = (depense.idGroupe, depense.titre, depense.description, depense.dateCreation, depense.montant)
    connexion.cursor.execute("INSERT INTO depense (idGroupe, titre, description, dateCreation, montant) VALUES (?, ?, ?, ?, ?)", values)
    depense.setId(connexion.cursor.lastrowid)

     
    