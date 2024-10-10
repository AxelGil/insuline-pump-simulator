class PumpConfig:
    def __init__(self, basal_rates, insulin_to_carb_ratio, min_sensitivity_factor, max_bolus, modes):
        self.basal_rates = basal_rates
        self.insulin_to_carb_ratio = insulin_to_carb_ratio
        self.min_sensitivity_factor = min_sensitivity_factor
        self.max_bolus = max_bolus
        self.modes = modes

    def validate(self):
        # Validation des taux basaux
        if not all(isinstance(rate, float) and rate >= 0 for rate in self.basal_rates):
            raise ValueError("Les taux basaux doivent être des nombres flottants positifs.")

        # Validation du ratio insuline/glucides
        if not isinstance(self.insulin_to_carb_ratio, float) or self.insulin_to_carb_ratio <= 0:
            raise ValueError("Le ratio insuline/glucides doit être un nombre flottant positif.")

        # Validation du facteur de sensibilité à l'insuline
        if not isinstance(self.min_sensitivity_factor, float) or self.min_sensitivity_factor <= 0:
            raise ValueError("Le facteur de sensibilité à l'insuline doit être un nombre flottant positif.")

        # Validation de la dose maximale de bolus
        if not isinstance(self.max_bolus, float) or self.max_bolus <= 0:
            raise ValueError("La dose maximale de bolus doit être un nombre flottant positif.")

        # Validation des modes
        if not isinstance(self.modes, dict):
            raise TypeError("Les modes doivent être un dictionnaire.")
        for mode_name, mode_config in self.modes.items():
            if not isinstance(mode_name, str):
                raise TypeError("Les noms de mode doivent être des chaînes de caractères.")
            if not isinstance(mode_config, dict):
                raise TypeError("Les configurations de mode doivent être des dictionnaires.")

        return True