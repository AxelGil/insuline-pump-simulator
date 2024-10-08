class Patient:
    def __init__(self, initial_glucose, carb_sensitivity, insulin_sensitivity):
        self.initial_glucose = initial_glucose
        self.glucose_level = initial_glucose
        self.carb_sensitivity = carb_sensitivity
        self.insulin_sensitivity = insulin_sensitivity

    def update_glucose_level(self, insulin, carbs):
        # Adjust the glucose level based on insulin and carbs consumed,
        # considering the patient's sensitivity to each
        self.glucose_level += (carbs * self.carb_sensitivity) - (insulin * self.insulin_sensitivity)

    def add_carbs(self, carbs):
        # Increase the glucose level based on the consumed carbs
        self.glucose_level += carbs * self.carb_sensitivity