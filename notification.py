import connexion, models, os, style

def viewNotifications(utilisateur):
    os.system('clear' if os.name == 'posix' else 'cls')
    style.showStyledTitle("Mes notifications")
    notifs = getNotificationsByUserId(utilisateur.id)
    if(len(notifs) == 0):
        print("\nVous n'avez pas de notifications\n")
    else:
        print("----------------------------------------------------------------------------")
        for notif in notifs:
            print(f"\nTitre   : {notif.titre}")
            print(f"\nDate    : {notif.date}")
            print(f"\nContenu : {notif.contenu}\n")
            print("----------------------------------------------------------------------------")
        connexion.cursor.execute("UPDATE recevoir_notification SET estVu = 1 WHERE idNotification = ? AND idUtilisateur = ? AND estVu = 0", (notif.id, utilisateur.id))

    input("Apopuyer entrer pour continuer ...")
    import main
    main.menuPrincipal(utilisateur)

def getNotificationsByUserId(userId):
    resources = connexion.cursor.execute("SELECT * FROM notification INNER JOIN recevoir_notification ON recevoir_notification.idNotification = notification.id WHERE recevoir_notification.idUtilisateur = ? ORDER BY notification.id DESC", (userId,))
    if(resources is None): return None
    notifications = []
    for resource in resources:
        notification = models.Notification(
            resource[1],
            resource[2],
            resource[3]
        ) 
        notification.setId(resource[0])
        notifications.append(notification)
    return notifications