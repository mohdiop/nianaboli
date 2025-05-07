import connexion
import models
def listerUtilisateurs():
    utilisateurs = connexion.con.execute("SELECT * FROM Utilisateur").fetchall()

    if not utilisateurs:
        print("Aucun utilisateur trouvé.")
        return

    print("Liste des utilisateurs :")
    for user in utilisateurs:
        id_utilisateur = user[0]
        nom = user[1]
        prenom = user[2]
        telephone = user[3]
        print(f"ID: {id_utilisateur}, Nom: {nom}, Prénom: {prenom}, Téléphone: {telephone}")
if __name__ == "__main__":
    listerUtilisateurs()