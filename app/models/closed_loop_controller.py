import time


class ClosedLoopController:
    def __init__(self, target_glucose, pump, cgm):
        self.target_glucose = target_glucose
        self.pump = pump
        self.cgm = cgm

    def adjust_basal_rate(self):
        current_glucose = self.cgm.measure_glucose(self.pump.patient)
        print(f"Current glucose: {current_glucose}, Target glucose: {self.target_glucose}")

        # Adjust basal rate based on the difference between current and target glucose
        # (You can implement your own logic here)
        if current_glucose > self.target_glucose:
            basal_rate = self.pump.calculate_basal_rate(current_glucose, self.target_glucose)
            print(f"Adjusted basal rate: {basal_rate}")
            return basal_rate
        else:
            return 0.0

    def control_loop(self):
        while True:
            # Measure current glucose
            current_glucose = self.cgm.measure_glucose(self.pump.patient)

            # Adjust basal rate
            basal_rate = self.adjust_basal_rate()

            # Deliver insulin
            self.pump.deliver_insulin(basal_rate)

            # Wait for the next measurement interval
            time.sleep(self.cgm.measurement_interval / 60)