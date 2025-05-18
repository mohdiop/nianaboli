# cursor = connexion.cursor
# def listPaie():
#     res= connexion.cursor.execute("""
#         SELECT paiement.id, paiement.montant, paiement.date, paiement.estValide,
#             utilisateur.prenom, utilisateur.nom,
#             depense.titre, depense.description
#         FROM paiement
#         INNER JOIN utilisateur ON utilisateur.id = paiement.idUtilisateur
#         INNER JOIN depense ON depense.id = paiement.idDepense
#     """)
#     res = cursor.fetchall()

#     if not res:
#         print("Aucun paiement pour le moment.")
#         return

#     print("\n--- Liste des paiements  ---")
#     for i, paiement in enumerate(res, start=1):
#         print(f"\nPaiement n°{i}")
#         print(f"Nom du redevable     : {paiement[5]}")  # nom
#         print(f"Prénom du redevable  : {paiement[4]}")  # prénom
#         print(f"Montant payé         : {paiement[1]}")
#         print(f"Date du paiement     : {paiement[2]}")
#         print(f"Titre de la dépense  : {paiement[6]}")
#         print(f"Description dépense  : {paiement[7]}")
#         print(f"Statut               : {'Non validé' if paiement[3] == 0 else 'Validé'}")
import sqlite3
from datetime import datetime

DB_NAME = "paiements.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS groupes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS membres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        groupe_id INTEGER NOT NULL,
        FOREIGN KEY (groupe_id) REFERENCES groupes(id)
    );

    CREATE TABLE IF NOT EXISTS depenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        montant REAL NOT NULL,
        date TEXT NOT NULL,
        payeur_id INTEGER NOT NULL,
        groupe_id INTEGER NOT NULL,
        FOREIGN KEY (payeur_id) REFERENCES membres(id),
        FOREIGN KEY (groupe_id) REFERENCES groupes(id)
    );
    """)
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée.")

def ajouter_groupe(nom):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groupes (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()
    print(f"✅ Groupe '{nom}' ajouté.")

def ajouter_membre(nom, groupe_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO membres (nom, groupe_id) VALUES (?, ?)", (nom, groupe_id))
    conn.commit()
    conn.close()
    print(f"👤 Membre '{nom}' ajouté au groupe ID {groupe_id}.")

def ajouter_depense(description, montant, payeur_id, groupe_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO depenses (description, montant, date, payeur_id, groupe_id)
        VALUES (?, ?, ?, ?, ?)
    """, (description, montant, date, payeur_id, groupe_id))
    conn.commit()
    conn.close()
    print(f"💰 Dépense '{description}' de {montant}FCFA enregistrée.")

def afficher_historique(groupe_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.description, d.montant, d.date, m.nom
        FROM depenses d
        JOIN membres m ON d.payeur_id = m.id
        WHERE d.groupe_id = ?
        ORDER BY d.date DESC
    """, (groupe_id,))
    resultats = cursor.fetchall()
    print(f"\n📜 Historique des paiements pour le groupe ID {groupe_id}:\n")
    if not resultats:
        print("Aucune dépense trouvée.")
    else:
        for row in resultats:
            print(f"🧾 {row[0]} | {row[1]}FCFA | {row[2]} | payé par {row[3]}")
    conn.close()

# -------- Interface console simple --------
def menu():
    init_db()
    while True:
        print("\n=== Menu ===")
        print("1. Ajouter un groupe")
        print("2. Ajouter un membre")
        print("3. Ajouter une dépense")
        print("4. Afficher l'historique")
        print("5. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            nom = input("Nom du groupe : ")
            ajouter_groupe(nom)
        elif choix == "2":
            nom = input("Nom du membre : ")
            groupe_id = int(input("ID du groupe : "))
            ajouter_membre(nom, groupe_id)
        elif choix == "3":
            desc = input("Description de la dépense : ")
            montant = float(input("Montant (FCFA) : "))
            payeur_id = int(input("ID du payeur : "))
            groupe_id = int(input("ID du groupe : "))
            ajouter_depense(desc, montant, payeur_id, groupe_id)
        elif choix == "4":
            groupe_id = int(input("ID du groupe à consulter : "))
            afficher_historique(groupe_id)
        elif choix == "5":
            break
        else:
            print("⛔ Choix invalide.")

# Lancer l'application
if __name__ == "__main__":
    menu()