import sqlite3
#class supprimer
def initialize():
    # Connexion à la base de données avec le mode autocommit activé
    conn = sqlite3.connect("nianaboli.db", isolation_level=None)
    cursor = conn.cursor()

    # Création de la table 'groupe'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groupe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        )
    ''')

    # Insertion de données dans la table 'groupe'
    groupe = [('Dépense 1',), ('Dépense 2',), ('Dépense 3',), ('Dépense 4',)]
    cursor.executemany('INSERT INTO groupe (nom) VALUES (?)', groupe)

    # Affichage des données avant suppression
    print("Groupe avant suppression :")
    cursor.execute('SELECT * FROM groupe')
    for row in cursor.fetchall():
        print(row)

    # Suppression des groupe avec les ID 2 et 4
    ids_to_delete = (2, 4)
    placeholders = ','.join(['?'] * len(ids_to_delete))
    query = f'DELETE FROM groupe WHERE id IN ({placeholders})'
    cursor.execute(query, ids_to_delete)

    # Affichage des données après suppression
    print("\nGroupe après suppression :")
    cursor.execute('SELECT * FROM groupe')
    for row in cursor.fetchall():
        print(row)

    # Fermeture de la connexion
    conn.close()

# Appel de la fonction
initialize()