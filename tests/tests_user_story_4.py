import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestsUserStory4(unittest.TestCase):

    def setUp(self):
        # Configuration initiale de la pompe à insuline
        self.config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7], 
            insulin_to_carb_ratio=10.0,  # 1 unité d'insuline pour 10g de glucides
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

    # Scénario : "Lecture continue de la glycémie"
    def test_continuous_glucose_reading(self):
        current_glucose = self.cgm.measure_glucose(self.patient)  # Simule la lecture du CGM
        self.assertTrue(isinstance(current_glucose, float), "La lecture du CGM doit être un float.")
        print(f"Test de lecture continue de la glycémie : Glycémie mesurée = {current_glucose} mg/dL.")

    # Scénario : "Ajustement automatique du débit basal"
    def test_automatic_adjustment_of_basal_rate(self):
        initial_basal_rate = self.pump.config.basal_rates[-1]
        self.controller.adjust_basal_rate(150)  # Simuler une glycémie de 150
        new_basal_rate = self.pump.config.basal_rates[-1]
        self.assertNotEqual(initial_basal_rate, new_basal_rate, "Le taux basal doit être ajusté.")
        print(f"Test d'ajustement automatique : Nouveau taux basal = {new_basal_rate} U/h.")

    # Scénario : "Confirmation des ajustements"
    def test_confirmation_of_adjustments(self):
        initial_glucose = self.cgm.measure_glucose(self.patient)
        self.controller.adjust_basal_rate(initial_glucose)  # Ajuster le débit basal basé sur la glycémie mesurée
        adjusted_glucose = self.cgm.measure_glucose(self.patient)  # Nouvelle lecture de la glycémie
        print(f"Confirmation : Glycémie initiale = {initial_glucose}, Glycémie après ajustement = {adjusted_glucose} mg/dL.")

    # Scénario : "Enregistrement des ajustements effectués"
    def test_recording_adjustments(self):
        initial_basal_rate = self.pump.config.basal_rates[-1]
        self.controller.adjust_basal_rate(150)  # Simuler une glycémie de 150
        new_basal_rate = self.pump.config.basal_rates[-1]
        # Simuler l'enregistrement dans l'historique (à implémenter selon ton design)
        print(f"Test d'enregistrement des ajustements : Ajustement de {initial_basal_rate} à {new_basal_rate} U/h.")

if __name__ == '__main__':
    unittest.main()
