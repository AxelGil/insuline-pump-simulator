import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestPumpConfiguration(unittest.TestCase):

    def setUp(self):
        # Configuration initiale de la pompe à insuline
        self.initial_config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7], 
            insulin_to_carb_ratio=10.0,  # 1 unité d'insuline pour 10g de glucides
            min_sensitivity_factor=30.0, 
            max_bolus=10.0, 
            modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
        )

        # Initialisation des objets nécessaires
        self.patient = Patient(initial_glucose=120, carb_intake=60, sensitivity=5, insulin_sensitivity=2)
        self.pump = InsulinPump(self.initial_config)
        self.cgm = CGM(measurement_interval=5)
        self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)
        self.pdm = PDM(pump=self.pump, config=self.initial_config, controller=self.controller, target_glucose=100)

    # Scénario : "Modification des taux basaux"
    def test_modify_basal_rates(self):
        new_basal_rates = [0.9, 0.7, 0.8]
        self.pdm.config.basal_rates = new_basal_rates  # Modification des taux basaux
        self.assertEqual(self.pdm.config.basal_rates, new_basal_rates)
        print(f"Test de modification des taux basaux réussi : {new_basal_rates}")

    # Scénario : "Modification du ratio insuline/glucides"
    def test_modify_insulin_to_carb_ratio(self):
        new_icr = 12.0  # Changement du ratio
        self.pdm.config.insulin_to_carb_ratio = new_icr
        self.assertEqual(self.pdm.config.insulin_to_carb_ratio, new_icr)
        print(f"Test de modification du ratio insuline/glucides réussi : {new_icr}")

    # Scénario : "Modification du facteur de sensibilité à l'insuline"
    def test_modify_insulin_sensitivity_factor(self):
        new_isf = 25.0  # Nouveau facteur de sensibilité
        self.pdm.config.min_sensitivity_factor = new_isf
        self.assertEqual(self.pdm.config.min_sensitivity_factor, new_isf)
        print(f"Test de modification du facteur de sensibilité réussi : {new_isf}")

    # Scénario : "Modification de la dose maximale de bolus"
    def test_modify_max_bolus(self):
        new_max_bolus = 8.0  # Nouvelle dose maximale
        self.pdm.config.max_bolus = new_max_bolus
        self.assertEqual(self.pdm.config.max_bolus, new_max_bolus)
        print(f"Test de modification de la dose maximale de bolus réussi : {new_max_bolus}")

    # Scénario : "Application des nouvelles configurations"
    def test_apply_new_configuration(self):
        new_config = PumpConfig(
            basal_rates=[1.0, 0.8, 0.6], 
            insulin_to_carb_ratio=15.0, 
            min_sensitivity_factor=25.0, 
            max_bolus=9.0, 
            modes={"jour": {"basal_increase": 0.2}, "nuit": {"basal_decrease": 0.1}}
        )
        self.pdm.apply_new_config(new_config)  # Appliquer la nouvelle configuration

        # Vérifications
        self.assertEqual(self.pdm.config.basal_rates, new_config.basal_rates)
        self.assertEqual(self.pdm.config.insulin_to_carb_ratio, new_config.insulin_to_carb_ratio)
        self.assertEqual(self.pdm.config.min_sensitivity_factor, new_config.min_sensitivity_factor)
        self.assertEqual(self.pdm.config.max_bolus, new_config.max_bolus)
        print("Test d'application de la nouvelle configuration réussi.")

if __name__ == '__main__':
    unittest.main()
