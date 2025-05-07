import createUser, sys, models

def login():
    print("Connexion\n\n")
    telephone = input("Votre numéro de téléphone: ")
    utilisateur = createUser.getUserByTel(telephone)
    while(utilisateur is None):
        telephone = input("Utilisateur introuvable! \nVérifiez votre numéro de téléphone: ")
        utilisateur = createUser.getUserByTel(telephone)

    motDePasse = input("Votre mot de passe: ")
    i = 0
    while(motDePasse != utilisateur.motDePasse):
        i = i+1
        motDePasse = input(f"Mot de passe incorrect! Tentative restant : {5-i} \nVotre mot de passe: ")
        if(i == 4):
            sys.exit("Nombre de tentative dépassé")
            
    return models.UtilisateurInfo(
        utilisateur.id,
        utilisateur.nom,
        utilisateur.prenom,
        utilisateur.telephone
    )

# query = "utilisateur(Telephone VARCHAR UNIQUE, Password VARCHAR)"

# cursor.execute(query)
# conn.commit()

# def enter(telephone, password):
#     query = "INSERT INTO utilisateur (Telephone, Password) VALUES (?, ?)"
#     cursor.execute(query, (telephone, password))
#     conn.commit()

# def check(telephone, password):
#     query = 'SELECT * FROM utilisateur WHERE Telephone = ? AND Password = ?'
#     cursor.execute(query, (telephone, password))
#     result = cursor.fetchone()
#     conn.commit()
#     print('[DEBUG][check] result:', result)
#     return result

# def loginlol():
#     answer = input("Login (Y/N): ")

#     if answer.lower() == "y":
#         telephone = input("Telephone: ")
#         password = input("Password: ")
#         if check(telephone, password):
#             print("Telephone correct!")
#             print("Password correct!")
#             print("Logging in...")
#         else:
#             print("Something wrong")

# # --- main ---

# conn = sqlite3.connect("nianaboli.db")
# cursor = conn.cursor()

# #create_table()

# Telephone = input("Create telephone: ")
# Password = input("Create password: ")

# enter(Telephone, Password)

# #check(Telephone, Password)

# loginlol()

# cursor.close()
# conn.close()
    