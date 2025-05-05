import sqlite3

con = sqlite3.connect("nianaboli.db")
con.autocommit = True 

def initialize(): 
    con.execute("CREATE TABLE IF NOT EXISTS essai (nombre)")
    con.execute("INSERT INTO essai (nombre) VALUES (1), (2), (3)")


def getAllNombre(): 
    res = con.execute("SELECT * FROM essai")
    return res