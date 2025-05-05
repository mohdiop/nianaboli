import sqlite3

con = sqlite3.connect("nianaboli.db")
con.autocommit = True 

def initialize():
    con.execute("CREATE TABLE IF NOT EXISTS " \
    "utilisateur (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, email TEXT UNIQUE, motDePasse TEXT)")
