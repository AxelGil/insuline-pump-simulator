class PompeInsuline:
    def ajusterTraitementAutomatique(self, taux_glucose):
        # Algorithme simplifié pour ajuster le dosage d'insuline
        if taux_glucose > 180:
            print("Augmentation du dosage d'insuline")
        elif taux_glucose < 70:
            print("Diminution du dosage d'insuline")
        else:
            print("Dosage d'insuline stable")