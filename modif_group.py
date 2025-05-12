from models import Groupe

def modifier_groupe():
    id_groupe = int(input("Entrez l'ID du groupe à modifier : "))
    nouveau_nom = input("Entrez le nouveau nom du groupe : ")

    groupe = Groupe(nouveau_nom, "", None)  # On n'a plus besoin de fournir un user
    groupe.setId(id_groupe)
    groupe.modifierNom(nouveau_nom)

    print("Nom du groupe mis à jour avec succès.")

if __name__ == "__main__":
    modifier_groupe()
