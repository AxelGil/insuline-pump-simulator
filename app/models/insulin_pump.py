import time
from app.models.pump_config import PumpConfig


class InsulinPump:
    def __init__(self, config: PumpConfig):
        self.config = config
        self.alarms = []  
        self.alarm_history = [] 

    def deliver_basal(self, hours: int):
        if not isinstance(hours, int):
            raise ValueError("Hours must be an integer.")
        total_basal = self.config.basal_rates[-1] * hours  # Direct multiplication
        print(f"Délivrance de {total_basal} UI d'insuline basale")
        return total_basal  # Return total insulin delivered
    
    def deliver_bolus(self, bolus: float):
        if bolus <= 0:
            raise ValueError("Bolus must be a positive number.")
        print(f"Delivering bolus of {bolus} UI of insulin.")

    def calculate_meal_bolus(self, carbs):
        bolus = carbs / self.config.insulin_to_carb_ratio
        print(f"Bolus alimentaire calculé : {bolus} UI")
        return bolus

    def calculate_correction_bolus(self, current_glucose, target_glucose):
        correction_bolus = (current_glucose-target_glucose) / self.config.min_sensitivity_factor
        print(f"bpmis alimentaire corrigé : {correction_bolus} UI")
        return correction_bolus

    def apply_configuration(self, config):
        self.config = config
        
    def activate_alarm(self, message):
        self.alarms.append(message)
        self.alarm_history.append({"message": message, "timestamp": time.time()})  # Record the alarm in history
        print(f"Alarm activated: {message}")

    def deactivate_alarm(self):
        if self.alarms:
            self.alarms.pop()  # Remove the most recent alarm
            print("Alarm deactivated.")

    def reset_alarm(self):
        self.alarms.clear()  # Clear all active alarms
        print("All alarms reset.")

    def get_active_alarms(self):
        return self.alarms  # Return current active alarms