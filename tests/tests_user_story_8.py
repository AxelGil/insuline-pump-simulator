import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestAlarmManagement(unittest.TestCase):

    def setUp(self):
        self.config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7],
            insulin_to_carb_ratio=10.0,
            min_sensitivity_factor=30.0,
            max_bolus=10.0,
            modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
        )

        self.patient = Patient(initial_glucose=120, carb_intake=60, sensitivity=5, insulin_sensitivity=2)
        self.pump = InsulinPump(self.config)
        self.cgm = CGM(measurement_interval=5)
        self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)
        self.pdm = PDM(pump=self.pump, config=self.config, controller=self.controller, target_glucose=100)

    def test_deactivate_alarm(self):
        self.patient.glucose_level = 250  # Simuler une glycémie élevée
        self.controller.adjust_basal_rate(self.patient.glucose_level)  # Déclenche une alarme
        self.pump.deactivate_alarm()  # Désactiver l'alarme
        self.assertFalse(self.pump.alarms, "Les alarmes devraient être désactivées.")
        print("Test de désactivation des alarmes réussi.")

    # def test_alarm_history_management(self):
    #     self.patient.glucose_level = 250  # Simuler une glycémie élevée
    #     self.controller.adjust_basal_rate(self.patient.glucose_level)  # Déclenche une alarme
    #     initial_history_length = len(self.controller.alarm_history)  # Longueur initiale de l'historique
    #     self.controller.deactivate_alarm()  # Désactiver l'alarme
    #     new_history_length = len(self.controller.alarm_history)  # Longueur après désactivation

    #     self.assertGreater(new_history_length, initial_history_length, "L'historique des alarmes devrait être mis à jour.")
    #     print("Test de gestion de l'historique des alarmes réussi.")

    def test_display_active_alarms(self):
        self.patient.glucose_level = 250  # Simuler une glycémie élevée
        self.controller.adjust_basal_rate(self.patient.glucose_level)  # Déclenche une alarme
        active_alarms = self.pump.get_active_alarms()  # Récupérer les alarmes actives
        self.assertTrue(len(active_alarms) > 0, "Il devrait y avoir des alarmes actives.")
        print("Test d'affichage des alarmes actives réussi.")

    def test_reset_alarm(self):
        self.patient.glucose_level = 250  # Simuler une glycémie élevée
        self.controller.adjust_basal_rate(self.patient.glucose_level)  # Déclenche une alarme
        self.pump.reset_alarm()  # Réinitialiser l'alarme
        self.assertTrue(not self.pump.alarms, "Les alarmes devraient être réinitialisées.")
        print("Test de réinitialisation des alarmes réussi.")

if __name__ == '__main__':
    unittest.main()

