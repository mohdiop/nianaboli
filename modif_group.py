from models import Groupe
import os, style, utilisateur

def modifier_groupe(groupe: Groupe, idUtilisateur):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitleCyan("Changement du nom du groupe")
    
    if(not utilisateur.estAdmin(idUtilisateur, groupe.id)):
        print("\nSeul l'administrateur peut modifier le nom du groupe\n")
        return
    
    print(f"Ancien nom du groupe : {groupe.nom}")
    nouveau_nom = input("Entrez le nouveau nom du groupe : ")
    
    groupe.modifierNom(nouveau_nom)
    groupe.nom = nouveau_nom

    print("Nom du groupe mis à jour avec succès.")
    return groupe
