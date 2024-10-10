import unittest
import json
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestDataExport(unittest.TestCase):

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

        # Populate history
        self.pdm.set_meal(60)  # 60g of carbs
        self.pump.deliver_bolus(6.0)  # Deliver a bolus of 6 UI
        self.patient.update_glucose(insulin=6.0, carbs=60)  # Update glucose level

    def test_export_data_history(self):
        confirmation_message, exported_data = self.pdm.export_data()  # Export the data
        self.assertTrue(isinstance(exported_data, str), "Les données exportées devraient être au format JSON (str).")
        
        # Verify that the exported data is not empty
        data_dict = json.loads(exported_data)
        self.assertIn("history", data_dict, "L'historique devrait être inclus dans les données exportées.")
        self.assertGreater(len(data_dict["history"]), 0, "L'historique exporté ne devrait pas être vide.")
        print("Test d'exportation des données réussi.")

    def test_export_format(self):
        confirmation_message, exported_data = self.pdm.export_data()  # Export the data
        data_dict = json.loads(exported_data)

        # Verify the structure of the exported data
        self.assertIn("history", data_dict)
        for entry in data_dict["history"]:
            self.assertIn("date", entry)
            self.assertIn("glucose", entry)
            self.assertIn("insulin", entry)
            self.assertIn("carbs", entry)
        print("Test de format d'exportation réussi.")

    def test_export_confirmation(self):
        confirmation_message, _ = self.pdm.export_data()  # Export the data
        self.assertEqual(confirmation_message, "Data export successful.", "La confirmation d'exportation devrait être réussie.")
        print("Test de confirmation d'exportation réussi.")

if __name__ == '__main__':
    unittest.main()
