class CGM:
    def __init__(self, measurement_interval):
        self.measurement_interval = measurement_interval
        self.current_glucose = 0

    def measure_glucose(self, patient):
        return patient.glucose_level
