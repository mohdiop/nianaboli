import connexion, models

def viewNotifications(utilisateur):
    print("--------------- Notifications ---------------")
    notifs = getNotificationsByUserId(utilisateur.id)
    if(notifs is None):
        print("\nVous n'avez pas de notifications\n")
    else:
        print("----------------------------------------------------------------------------")
        for notif in notifs:
            print(f"\nTitre       : {notif.titre}")
            print(f"\nContenu     : {notif.contenu}\n")
        print("----------------------------------------------------------------------------")

    import main
    main.menuPrincipal(utilisateur)

def getNotificationsByUserId(userId):
    resources = connexion.cursor.execute("SELECT * FROM notification INNER JOIN recevoir_notification ON recevoir_notification.idNotification = notification.id WHERE recevoir_notification.idUtilisateur = ? AND recevoir_notification.estVu = 0", (userId,))
    if(resources is None): return None
    notifications = []
    for resource in resources:
        notification = models.Notification(
            resource[1],
            resource[2]
        ) 
        notifications.append(notification)
    return notifications