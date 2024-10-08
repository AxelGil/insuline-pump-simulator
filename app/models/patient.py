class Patient:
    def __init__(self, initial_glucose):
        self.glucose_level = initial_glucose

    def update_glucose_level(self, insulin, carbs):
        self.glucose_level += (carbs * 5) - (insulin * 2)
