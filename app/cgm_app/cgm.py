import random

class CapteurGlucose:
    def mesurer(self):
        # Simulation d'une mesure aléatoire (à remplacer par une vraie mesure)
        taux_glucose = random.randint(60, 180)
        return taux_glucose

    def transmettreDonnees(self, recepteur):
        taux_glucose = self.mesurer()
        recepteur.recevoirDonnees(taux_glucose)

    def configurer(self, unite_mesure='mg/dL'):
        self.unite_mesure = unite_mesure    