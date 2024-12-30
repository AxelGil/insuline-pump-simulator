from enum import EJECT
import sqlite3
import requests

from app.cgm_app.cgm import CapteurGlucose


class RecepteurDedie:
    def __init__(self, user, cgm: CapteurGlucose):
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        self.historique_donnees = cursor.execute("SELECT * FROM user_basal_rate WHERE id_user = (SELECT id FROM users WHERE name = ?)", (user,)).fetchall()

    def _fetch_data_from_cgm(self, endpoint):
        try:
            response = requests.get(f"{self.cgm_base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()  # Retourne les données au format JSON
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None
        
    
        
    def recevoirDonnees(self):
        data = self._fetch_data_from_cgm("data")
        if data:
            # Exemple de logique pour recevoir les données
            print(f"Données reçues : {data}")
            return data
        else:
            print("Impossible de recevoir les données, aucune donnée récupérée.")
            return None
        
    def afficherDonnees(self):
        print(self.historique_donnees)