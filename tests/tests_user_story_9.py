import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestDataMonitoring(unittest.TestCase):

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

    # Scénario : "Analyse des données de glycémie"
    def test_analyze_glucose_trend(self):
        # Simuler des lectures de glycémie pour créer une tendance
        glucose_readings = [120, 125, 130, 140, 135, 150]  # Simuler une tendance à la hausse
        for reading in glucose_readings:
            self.patient.glucose_level = reading
            self.cgm.measure_glucose(self.patient)  # Mise à jour des lectures de glycémie
            self.controller.adjust_basal_rate(reading)  # Ajustement du débit basal

        # Vérification de la tendance
        trend = self.controller.analyze_glucose_trend()  # Méthode à implémenter pour analyser la tendance
        self.assertEqual(trend, "Increasing", "La tendance de la glycémie devrait être à la hausse.")
        print("Test d'analyse des données de glycémie réussi : Tendance à la hausse détectée.")

    # Scénario : "Notification des tendances"
    def test_notify_patient_of_trend(self):
        # Simuler des lectures de glycémie pour créer une tendance
        glucose_readings = [120, 130, 140, 180, 250]  # Simuler une tendance à la hausse
        for reading in glucose_readings:
            self.patient.glucose_level = reading
            self.cgm.measure_glucose(self.patient)  # Mettre à jour les lectures de glycémie
            self.controller.adjust_basal_rate(reading)  # Ajustement du débit basal

        notification = self.controller.notify_patient_of_trend()  # Notification de tendance
        self.assertIn("High blood sugar trend detected", notification, "Le patient devrait être notifié d'une tendance élevée.")
        print("Test de notification de tendance réussi.")

    # Scénario : "Affichage d'un résumé des tendances"
    def test_display_trend_summary(self):
        # Simuler des lectures de glycémie pour créer des tendances
        glucose_readings = [120, 125, 130, 140, 135, 150]
        for reading in glucose_readings:
            self.patient.glucose_level = reading
            self.cgm.measure_glucose(self.patient)  # Mise à jour des lectures de glycémie
            self.controller.adjust_basal_rate(reading)  # Ajustement du débit basal

        summary = self.controller.display_trend_summary()  # Méthode à implémenter pour afficher le résumé
        self.assertTrue("Increasing" in summary, "Le résumé devrait contenir l'information sur la tendance à la hausse.")
        print("Test d'affichage du résumé des tendances réussi.")


if __name__ == '__main__':
    unittest.main()
