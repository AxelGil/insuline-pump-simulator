class ClosedLoopController:
    def __init__(self, target_glucose, pump, cgm):
        self.target_glucose = target_glucose
        self.pump = pump
        self.cgm = cgm

    def adjust_basal_rate(self):
        current_glucose = self.cgm.measure_glucose(self.pump.patient)
        if current_glucose > self.target_glucose:
            correction_bolus = self.pump.calculate_correction_bolus(current_glucose, self.target_glucose)
            return correction_bolus
        return 0.0
