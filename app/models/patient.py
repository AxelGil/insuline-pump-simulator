class Patient:
    def __init__(self, initial_glucose, carb_intake, sensitivity, insulin_sensitivity):
        self.glucose_level = initial_glucose
        self.carb_intake = carb_intake
        self.sensitivity = sensitivity
        self.insulin_sensitivity = insulin_sensitivity

    def update_glucose(self, insulin, carbs):
        self.glucose_level -= insulin * self.insulin_sensitivity
        self.glucose_level += carbs * self.sensitivity
        pass

    def add_carbs(self, carbs):
        self.glucose_level += carbs * self.sensitivity
        pass