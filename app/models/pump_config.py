class PumpConfig:
    def __init__(self, basal_rates, insulin_to_carb_ratio, insulin_sensitivity_factor, max_bolus):
        self.basal_rates = basal_rates
        self.insulin_to_carb_ratio = insulin_to_carb_ratio
        self.insulin_sensitivity_factor = insulin_sensitivity_factor
        self.max_bolus = max_bolus

    def validate(self) -> bool:
        return all(rate >= 0 for rate in self.basal_rates) and self.max_bolus > 0
