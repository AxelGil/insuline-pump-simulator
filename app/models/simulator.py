class Simulator:
    def __init__(self, patient, pump, cgm, controller, pdm, duration):
        self.patient = patient
        self.pump = pump
        self.cgm = cgm
        self.controller = controller
        self.pdm = pdm
        self.duration = duration

    def run_simulation(self):
        results = []
        for hour in range(self.duration):
            # Measure current glucose
            current_glucose = self.cgm.measure_glucose(self.patient)

            # Adjust basal rate
            basal_rate = self.controller.adjust_basal_rate(current_glucose)

            # Deliver insulin
            self.pump.deliver_insulin(basal_rate)

            # Update patient's glucose level
            self.patient.update_glucose_level(basal_rate, 0)

            # Log data
            self.log_data(hour, current_glucose, basal_rate)

            results.append((hour, current_glucose, basal_rate))

        return results

    def log_data(self, hour, current_glucose, basal_rate):
        # Log data to a file or database
        with open("simulation_data.csv", "a") as f:
            f.write(f"{hour},{current_glucose},{basal_rate}\n")