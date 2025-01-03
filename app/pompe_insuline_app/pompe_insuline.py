class PompeInsuline:
    def ajusterTraitementAutomatique(taux_glucose):
        # Algorithme simplifié pour ajuster le dosage d'insuline
        if taux_glucose > 180:
            return "Augmentation du dosage d'insuline"
        elif taux_glucose < 70:
            return "Diminution du dosage d'insuline"
        else:
            return "Dosage d'insuline stable"