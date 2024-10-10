import time
from app.models.cgm import CGM
from app.models.insulin_pump import InsulinPump
from app.models.patient import Patient


class ClosedLoopController:
    def __init__(self, target_glucose, insulin_pump: InsulinPump, cgm: CGM):
        self.target_glucose = target_glucose
        self.insulin_pump = insulin_pump
        self.cgm = cgm
        self.glucose_history = []  # To store glucose readings for trend analysis

    def adjust_basal_rate(self, current_glucose):
        error = self.target_glucose - current_glucose
        kp = 0.01  # Adjust the gain here for better results
        delta_basal = kp * error
        new_basal_rate = self.insulin_pump.config.basal_rates[-1] + delta_basal
        
        min_basal_rate = 0.2  # Minimum basal rate
        max_basal_rate = 2.0  # Maximum basal rate
        new_basal_rate = max(min_basal_rate, new_basal_rate)  # Lower limit
        new_basal_rate = min(max_basal_rate, new_basal_rate)  # Upper limit
        
         # Check for alarm conditions
        if current_glucose < 70:  # Low blood sugar condition
            self.insulin_pump.activate_alarm("Low blood sugar!")
        elif current_glucose > 180:  # High blood sugar condition
            self.insulin_pump.activate_alarm("High blood sugar!")

        # Apply new basal rate
        self.insulin_pump.config.basal_rates[-1] = new_basal_rate
        
        # Store glucose reading for trend analysis
        self.glucose_history.append(current_glucose)  # Store current glucose
        
        return new_basal_rate

    def control_loop(self, patient: Patient):
        while True:
            current_glucose = self.cgm.measure_glucose(patient)

            # Ajuster le débit basal
            self.adjust_basal_rate(current_glucose)

            # Attendre l'intervalle de mesure suivant
            time.sleep(self.cgm.measurement_interval * 60)
            
    def analyze_glucose_trend(self):
        if len(self.glucose_history) < 2:
            return "Insufficient data"

        # Simple trend analysis
        if self.glucose_history[-1] > self.glucose_history[-2]:
            return "Increasing"
        elif self.glucose_history[-1] < self.glucose_history[-2]:
            return "Decreasing"
        else:
            return "Stable"

    def notify_patient_of_trend(self):
        if len(self.glucose_history) < 2:
            return "Not enough data to determine trend."
        
        trend = self.analyze_glucose_trend()
        if trend == "Increasing" and self.glucose_history[-1] > 180:
            notification = "High blood sugar trend detected."
        elif trend == "Decreasing" and self.glucose_history[-1] < 70:
            notification = "Low blood sugar trend detected."
        else:
            notification = f"Current trend: {trend}."

        print(notification)
        return notification

    def display_trend_summary(self):
        trend = self.analyze_glucose_trend()
        summary = f"Current trend: {trend}. Last 5 readings: {self.glucose_history[-5:] if len(self.glucose_history) >= 5 else self.glucose_history}"
        print(summary)
        return summary