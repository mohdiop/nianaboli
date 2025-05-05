import sqlite3

def initialize():
    con = sqlite3.connect("nianaboli.db")
    con.autocommit = True 