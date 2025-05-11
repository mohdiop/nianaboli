from datetime import date
from models import Depense

def main():
    try:
        # Demande de l'utilisateur
        idGroupe = int(input("ID du groupe concerné : "))
        titre = input("Titre de la dépense : ")
        description = input("Description : ")
        montant = int(input("Montant total de la dépense : "))

        # Créer une instance de Depense
        depense = Depense(idGroupe, montant, titre, description, date.today().strftime("%d/%m/%Y"))
        depense.enregistrer()  # Enregistrer la dépense dans la base de données

        # Appeler la méthode repartir_automatiquement pour répartir la dépense
        depense.repartir_automatiquement()  # Appel à la méthode qui répartit la dépense

    except Exception as e:
        print("Une erreur est survenue :", e)

if __name__ == "__main__":
    main()
