from app.dexcom_platform_app.dexcom_platform import DexcomPlatform
import requests


class DexcomFollow:
  
    def __init__(self, platform: DexcomPlatform):
        self.platform = platform
        pass
    
    def _fetch_data_from_platform(self, endpoint):
        try:
            response = requests.get(f"{self.platform_base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()  # Retourne les données au format JSON
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None
      
    def suivreDonnees(self):
        data = self._fetch_data_from_platform("data")
        if data:
            # Exemple de logique pour suivre les données
            print(f"Données suivies : {data}")
            return data
        else:
            print("Impossible de suivre les données, aucune donnée récupérée.")
            return None
        pass

    def notificationsEnTempsReel(self):
        
        pass