import sqlite3

class DexcomPlatform:
  
    def __init__(self):
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()
    
    def afficherDonnees(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        pass

    def envoyerAlertesPersonnalisees(self):
        # Code pour envoyer des alertes personnalisées
        pass
      
    def getDonneeUser(self, user):
        self.cursor.execute("SELECT * FROM user_basal_rate WHERE id_user = ?", (user,))
        row = self.cursor.fetchone()
        return row

    def synchroniserDonnees(self, user, basal_rate):
        self.cursor.execute("INSERT INTO user_basal_rate (id_user, basal_rate) VALUES (?, ?)", (user, basal_rate))