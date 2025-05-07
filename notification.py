import sqlite3

def create_notification_table():
    conn = sqlite3.connect("nianaboli.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def send_predefined_notification():
    conn = sqlite3.connect("nianaboli.db")
    cursor = conn.cursor()
    message = "Vous venez d'être ajouté à un groupe de dépense."
    cursor.execute("INSERT INTO notification (message) VALUES (?)", (message,))
    conn.commit()
    print("Notification envoyée.")
    conn.close()

if __name__ == "__main__":
    create_notification_table()
    send_predefined_notification()
