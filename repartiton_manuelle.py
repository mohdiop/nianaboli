from models import Depense
from datetime import date

def saisir_repartition():
    repartition = {}
    while True:
        try:
            id_user = int(input("ID de l'utilisateur (ou 0 pour terminer) : "))
            if id_user == 0:
                break
            montant = int(input(f"Montant à payer pour l'utilisateur {id_user} : "))
            repartition[id_user] = montant
        except ValueError:
            print("Entrée invalide. Essayez encore.")
    return repartition

def main():
    id_groupe = int(input("ID du groupe concerné : "))
    titre = input("Titre de la dépense : ")
    description = input("Description : ")
    montant_total = int(input("Montant total de la dépense : "))

    depense = Depense(id_groupe, montant_total, titre, description, date.today().strftime("%d/%m/%Y"))
    depense.enregistrer()

    print("\n--- Répartition manuelle ---")
    repartition = saisir_repartition()
    depense.repartir_manuellement(repartition)
    print("Répartition effectuée.")

if __name__ == "__main__":
    main()
