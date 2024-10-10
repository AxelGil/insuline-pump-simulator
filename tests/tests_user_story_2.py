import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient


class TestsUserStory2(unittest.TestCase):

    def setUp(self):
        # Initialisation des configurations de la pompe à insuline
        self.config = PumpConfig(
            basal_rates=[0.8, 0.6, 0.7],  # taux basaux
            insulin_to_carb_ratio=10.0, 
            min_sensitivity_factor=30.0,  # ISF
            max_bolus=10.0, 
            modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
        )

        # Configuration du patient et des composants de la pompe
        self.patient = Patient(initial_glucose=120, carb_intake=60, sensitivity=5, insulin_sensitivity=2)
        self.pump = InsulinPump(self.config)
        self.cgm = CGM(measurement_interval=5)
        self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)

    # Scénario : "Ajustement des taux basaux selon les réglages du PDM"
    def test_adjust_basal_rate_based_on_config(self):
        current_glucose = 90  # Glycémie actuelle
        new_basal_rate = self.controller.adjust_basal_rate(current_glucose)
        self.assertAlmostEqual(new_basal_rate, 0.8, delta=0.1)  # Test du taux basaux ajusté
        print(f"Test d'ajustement du taux basal : Nouveau taux basal = {new_basal_rate} U/h")

    # Scénario : "Correction glycémique basée sur le CGM"
    def test_correction_based_on_cgm(self):
        current_glucose = 180  # Glycémie mesurée par le CGM
        correction_bolus = self.pump.calculate_correction_bolus(current_glucose, self.controller.target_glucose)
        self.assertAlmostEqual(correction_bolus, 2.67, places=2)  # Calcul du bolus de correction
        print(f"Test de correction basé sur CGM : Bolus de correction = {correction_bolus} U")

    # # Scénario : "Ajustement en fonction de la tendance glycémique"
    # def test_adjustment_based_on_trend(self):
    #   # Simulate a trend where glucose is increasing significantly
    #   glucose_readings = [110, 140, 160, 190]  # Simulation d'une forte augmentation de la glycémie
    #   for reading in glucose_readings:
    #       self.cgm.current_glucose = reading
    #       new_basal_rate = self.controller.adjust_basal_rate(reading)
    #   self.assertTrue(new_basal_rate > 0.7)  # Vérifier que le taux basaux a augmenté en réponse à la tendance
    #   print(f"Test d'ajustement en fonction de la tendance : Nouveau taux basal = {new_basal_rate} U/h")


    # Scénario : "Administration des doses ajustées"
    def test_administration_of_adjusted_doses(self):
      hours = 1  # Duration simulated in hours
      current_basal_rate = self.pump.config.basal_rates[-1]  # Get current basal rate before delivery
      total_basal_delivered = self.pump.deliver_basal(hours)
      self.assertAlmostEqual(total_basal_delivered, current_basal_rate, delta=0.1)
      print(f"Test d'administration des doses : Total basal délivré = {total_basal_delivered} U")


if __name__ == '__main__':
    unittest.main()
