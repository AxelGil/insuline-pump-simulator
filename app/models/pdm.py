import json
import time
from app.models.closed_loop_controller import ClosedLoopController
from app.models.insulin_pump import InsulinPump
from app.models.pump_config import PumpConfig


class PDM:
    def __init__(self, pump: InsulinPump, config: PumpConfig, controller: ClosedLoopController, target_glucose):
        self.pump = pump
        self.config = config
        self.controller = controller
        self.target_glucose = target_glucose
        self.history = []
    
    def set_meal(self, carbs):
        bolus = self.pump.calculate_meal_bolus(carbs)
        self.pump.deliver_bolus(bolus)
        # Add entry to history
        self.history.append({
            "date": time.time(),
            "glucose": self.pump.config.basal_rates[-1],  # Assuming the last basal rate as current glucose
            "insulin": bolus,
            "carbs": carbs
        })

    def set_target_glucose(self, target):
        self.target_glucose = target
        self.controller.target_glucose = target

    def apply_new_config(self, config):
        self.config = config
        self.pump.apply_configuration(config)

    def add_alarm(self, alarm):
        self.alarms.append(alarm)

    def view_history(self):
        print("Historique des données :")
        for entry in self.history:
            print(f"Date : {entry['date']}")
            print(f"Glycémie : {entry['glucose']} mg/dL")
            print(f"Insuline : {entry['insulin']} U")
            print(f"Repas : {entry['carbs']} g")
            print("-" * 20)

    def set_mode(self, mode, config):
        self.current_mode = mode
        # Appliquer les configurations spécifiques au mode
        if mode == "nuit":
            self.controller.target_glucose = 100  # Exemple de configuration pour le mode nuit
            self.pump.config.basal_rate = 0.5  # Exemple de configuration pour le mode nuit
        elif mode == "jour":
            self.controller.target_glucose = 50
            self.pump.config.basal_rates = 0.5
        else:
            print("Mode non reconnu")
            
    def export_data(self):
        # Export history to JSON
        data = {"history": self.history}
        json_data = json.dumps(data)  # Convert history to JSON format
        return "Data export successful.", json_data  # Return a success message along with JSON data