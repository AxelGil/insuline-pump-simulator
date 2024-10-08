class PumpConfig:
    def __init__(self, basal_rates=None, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10):
        if basal_rates is None:
            basal_rates = [0] * 24  # Default to 0 for all 24 hours
        self.basal_rates = basal_rates  # List of basal rates by hour
        self.insulin_to_carb_ratio = insulin_to_carb_ratio  # Insulin-to-carb ratio
        self.insulin_sensitivity_factor = insulin_sensitivity_factor  # Insulin sensitivity factor
        self.max_bolus = max_bolus  # Maximum bolus allowed
        self.custom_modes = {}  # Dictionary to hold custom modes

    def validate(self) -> bool:
        return (
            len(self.basal_rates) == 24 and
            all(rate >= 0 for rate in self.basal_rates) and
            self.max_bolus > 0
        )

    def set_custom_mode(self, mode_name, parameters):
        """Sets custom modes for the pump based on parameters provided."""
        self.custom_modes[mode_name] = parameters
