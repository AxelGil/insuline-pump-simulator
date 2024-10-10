import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestsUserStory5(unittest.TestCase):

    def setUp(self):
        # Configuration initiale de la pompe à insuline
        self.config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7], 
            insulin_to_carb_ratio=10.0,
            min_sensitivity_factor=30.0, 
            max_bolus=10.0, 
            modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
        )

        # Initialisation des objets nécessaires
        self.patient = Patient(initial_glucose=120, carb_intake=60, sensitivity=5, insulin_sensitivity=2)
        self.pump = InsulinPump(self.config)
        self.cgm = CGM(measurement_interval=5)
        self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)
        self.pdm = PDM(pump=self.pump, config=self.config, controller=self.controller, target_glucose=100)

    # Scénario : "Détection des valeurs de glycémie critiques"
    def test_glucose_alarm_detection_high(self):
        self.patient.glucose_level = 250  # Simuler une glycémie trop élevée
        alarm_triggered = self.controller.adjust_basal_rate(self.patient.glucose_level)
        self.assertTrue(alarm_triggered, "L'alarme devrait se déclencher pour une glycémie trop élevée.")
        print("Test de détection des alarmes pour glycémie élevée réussi.")

    def test_glucose_alarm_detection_low(self):
        self.patient.glucose_level = 50  # Simuler une glycémie trop basse
        alarm_triggered = self.controller.adjust_basal_rate(self.patient.glucose_level)
        self.assertTrue(alarm_triggered, "L'alarme devrait se déclencher pour une glycémie trop basse.")
        print("Test de détection des alarmes pour glycémie basse réussi.")

    # Scénario : "Notification au patient"
    def test_notification_to_patient(self):
        self.patient.glucose_level = 250  # Simuler une glycémie trop élevée
        alarm_triggered = self.controller.adjust_basal_rate(self.patient.glucose_level)
        if alarm_triggered:
            print("Notification au patient : Alarme de glycémie élevée activée.")
        self.assertTrue(alarm_triggered, "Le patient devrait recevoir une notification d'alarme.")

    # Scénario : "Gestion des alarmes"
    # def test_alarm_history_management(self):
    #     initial_history_length = len(self.pump.alarms)  # Longueur historique avant l'alarme
    #     self.patient.glucose_level = 250  # Simuler une glycémie trop élevée
    #     self.controller.adjust_basal_rate(self.patient.glucose_level)
    #     new_history_length = len(self.pump.alarms)  # Longueur après l'alarme
    #     self.assertGreater(new_history_length, initial_history_length, "L'historique des alarmes devrait être mis à jour.")
    #     print(f"Test de gestion des alarmes : Historique mis à jour, longueur actuelle = {new_history_length}.")

if __name__ == '__main__':
    unittest.main()
