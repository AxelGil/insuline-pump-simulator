import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.pdm import PDM


class UserStory1(unittest.TestCase):

    def setUp(self):
        # Configuration initiale de la pompe avec des valeurs valides
        self.config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7], 
            insulin_to_carb_ratio=10.0, 
            min_sensitivity_factor=30.0, 
            max_bolus=10.0, 
            modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
        )

        self.pump = InsulinPump(self.config)
        self.cgm = CGM(measurement_interval=5)
        self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)
        self.pdm = PDM(pump=self.pump, config=self.config, controller=self.controller, target_glucose=100)

    def test_configure_basal_rates(self):
        # Test de la configuration des taux basaux par heure
        new_basal_rates = [0.9, 0.7, 0.6, 0.8, 1.0]
        self.config.basal_rates = new_basal_rates
        self.assertEqual(self.pdm.config.basal_rates, new_basal_rates)
        print("Test de configuration des taux basaux réussi.")

    def test_configure_insulin_to_carb_ratio(self):
        # Test de la configuration du ratio insuline/glucides (ICR)
        new_icr = 12.0
        self.config.insulin_to_carb_ratio = new_icr
        self.assertEqual(self.pdm.config.insulin_to_carb_ratio, new_icr)
        print("Test de configuration du ratio insuline/glucides réussi.")

    def test_configure_sensitivity_factor(self):
        # Test de la configuration du facteur de sensibilité à l'insuline (ISF)
        new_isf = 35.0
        self.config.min_sensitivity_factor = new_isf
        self.assertEqual(self.pdm.config.min_sensitivity_factor, new_isf)
        print("Test de configuration du facteur de sensibilité réussi.")

    def test_configure_max_bolus(self):
        # Test de la configuration de la dose maximale de bolus
        new_max_bolus = 8.0
        self.config.max_bolus = new_max_bolus
        self.assertEqual(self.pdm.config.max_bolus, new_max_bolus)
        print("Test de configuration de la dose maximale de bolus réussi.")

    def test_configure_modes(self):
        # Test de la configuration des modes personnalisés
        new_modes = {"nuit": {"basal_decrease": 0.15}}
        self.config.modes = new_modes
        self.assertEqual(self.pdm.config.modes, new_modes)
        print("Test de configuration des modes personnalisés réussi.")


if __name__ == '__main__':
    unittest.main()
