class InsulinPump:
    def __init__(self, config, patient):
        """
        Initializes the insulin pump with its configuration and associated patient.

        :param config: Configuration of the insulin pump
        :param patient: Instance of the Patient class
        """
        self.config = config
        self.patient = patient  # Add the patient reference
        self.alarms = []

    def deliver_basal(self, hour):
        if hour < len(self.config.basal_rates):
            return self.config.basal_rates[hour]
        return 0.0

    def calculate_meal_bolus(self, carbs):
        return carbs / self.config.insulin_to_carb_ratio

    def calculate_correction_bolus(self, current_glucose, target_glucose):
        if current_glucose > target_glucose:
            insulin_needed = (current_glucose - target_glucose) / self.config.insulin_sensitivity_factor
            return min(insulin_needed, self.config.max_bolus)
        return 0.0
