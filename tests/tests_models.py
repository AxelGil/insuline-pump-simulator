import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.patient import Patient
from app.models.cgm import CGM
from app.models.closed_loop_controller import ClosedLoopController
from app.models.simulator import Simulator

class TestInsulinPumpSimulator(unittest.TestCase):
    
    def setUp(self):
        # Setup for all tests
        self.basal_rates = [0.8, 0.6, 0.5] + [0] * 21  # Example basal rates for 24 hours
        self.config = PumpConfig(self.basal_rates, 10, 30, 10)
        self.patient = Patient(120)
        self.pump = InsulinPump(self.config, self.patient)
        self.cgm = CGM(5)
        self.controller = ClosedLoopController(120, self.pump, self.cgm)
        self.simulator = Simulator(self.patient, self.pump, self.cgm, self.controller)

    def test_pump_configuration(self):
        # Test if configuration is valid
        self.assertTrue(self.config.validate())
        self.config.basal_rates[0] = -1  # Invalid rate
        self.assertFalse(self.config.validate())

    def test_set_custom_mode(self):
        # Test setting custom modes
        self.config.set_custom_mode('night', {'basal_rate': 0.5, 'isf': 20, 'icr': 8})
        self.assertIn('night', self.config.custom_modes)
        self.assertEqual(self.config.custom_modes['night'], {'basal_rate': 0.5, 'isf': 20, 'icr': 8})

    def test_deliver_basal(self):
        # Test basal delivery
        for hour, expected_rate in enumerate(self.basal_rates):
            self.assertEqual(self.pump.deliver_basal(hour), expected_rate)

    def test_calculate_meal_bolus(self):
        # Test meal bolus calculation
        self.assertEqual(self.pump.calculate_meal_bolus(60), 6)  # 60g carbs

    def test_calculate_correction_bolus(self):
        # Test correction bolus calculation
        self.assertEqual(self.pump.calculate_correction_bolus(150, 120), 1)

    def test_update_glucose_level(self):
        # Test glucose level update
        self.patient.update_glucose_level(2, 60)  # 2 units of insulin, 60 grams of carbs
        self.assertAlmostEqual(self.patient.glucose_level, 120 + (60 * 5) - (2 * 2), places=2)

    def test_cgm_measurement(self):
        # Test CGM glucose measurement
        self.assertEqual(self.cgm.measure_glucose(self.patient), 120)

    def test_run_simulation(self):
        # Test the entire simulation process
        results = self.simulator.run_simulation()
        self.assertEqual(len(results), 24)  # Should run for 24 hours
        for hour, glucose in results:
            self.assertIsInstance(hour, int)
            self.assertIsInstance(glucose, float)

    def test_adjust_basal_rate(self):
        self.cgm.current_glucose = 1
        correction = self.controller.adjust_basal_rate()
        self.assertGreater(correction, 0)


if __name__ == '__main__':
    unittest.main()
