class Simulator:
    def __init__(self, patient, pump, cgm, controller):
        self.patient = patient
        self.pump = pump
        self.cgm = cgm
        self.controller = controller
        self.duration = 24

    def run_simulation(self):
        results = []
        for hour in range(self.duration):
            basal = self.pump.deliver_basal(hour)
            self.patient.update_glucose_level(basal, 0)
            correction = self.controller.adjust_basal_rate()
            self.patient.update_glucose_level(correction, 0)
            results.append((hour, self.patient.glucose_level))

        return results
