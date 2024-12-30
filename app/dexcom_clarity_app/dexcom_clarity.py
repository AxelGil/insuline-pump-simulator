import requests
class DexcomClarity:
    
    def _fetch_data_from_platform(self, endpoint):
        try:
            response = requests.get(f"{self.platform_base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()  # Retourne les données au format JSON
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None
        
    def analyserTendances(self):
        data = self._fetch_data_from_platform("data/trends")
        if data:
            tendances = {"moyenne_glucose": sum(data) / len(data)}
            print(f"Tendances analysées : {tendances}")
            return tendances
        else:
            print("Impossible d'analyser les tendances, aucune donnée récupérée.")
            return None

    def genererRapports(self):
        data = self._fetch_data_from_platform("data/reports")
        if data:
            rapport = f"Rapport généré avec {len(data)} entrées."
            print(rapport)
            return rapport
        else:
            print("Impossible de générer un rapport, aucune donnée récupérée.")
            return None

    def partagerDonnees(self):
        data = self._fetch_data_from_platform("data/share")
        if data:
            # Exemple de partage des données
            print(f"Les données suivantes ont été partagées : {data}")
            return True
        else:
            print("Impossible de partager les données, aucune donnée récupérée.")
            return False
        pass