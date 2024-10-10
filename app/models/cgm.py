import random

from app.models.patient import Patient


class CGM:
    def __init__(self, measurement_interval):
        self.measurement_interval = measurement_interval

    def measure_glucose(self, patient: Patient):
        noise = random.uniform(-0.1, 0.1) 
        self.current_glucose = patient.glucose_level + noise
        return self.current_glucose