import connexion
import models
from datetime import datetime

def creation_depense(id_createur_depense, id_groupe):
    cursor = connexion.cursor()

    # Vérifie que le demandeur est administrateur du groupe
    cursor.execute("""
        SELECT 1 FROM appartenance
        WHERE idUtilisateur = ? AND idGroupe = ? AND role = 'ADMINISTRATEUR'
    """, (id_createur_depense, id_groupe))
    est_admin = cursor.fetchone()

    if not est_admin:
        return " Seul un administrateur peut créer une dépense."

    print("=== Création d'une dépense ===")
    titre = input("Titre de la dépense : ")
    description = input("Description de la dépense : ")
    
    try:
        montant = int(input("Montant de la dépense  : "))
    except ValueError:
        return " Le montant doit être un entier."

    date = datetime.now().strftime("%Y-%m-%d")

    # Création de l'objet dépense (ajuste selon ta classe)
    depense = models.Depense(montant, titre, description, date, id_groupe)

    # Appel à la méthode pour insérer en BDD
    resultat = depense.creerDepense()  # Assure-toi que cette méthode existe

    return resultat or "Dépense créée avec succès."

     
    