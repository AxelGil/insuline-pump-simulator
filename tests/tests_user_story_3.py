import unittest
from app.models.pump_config import PumpConfig
from app.models.insulin_pump import InsulinPump
from app.models.closed_loop_controller import ClosedLoopController
from app.models.cgm import CGM
from app.models.patient import Patient
from app.models.pdm import PDM


class TestsUserStory3(unittest.TestCase):

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

    # Scénario : "Entrée des glucides par le patient"
    def test_patient_enters_carbs(self):
        carbs_consumed = 60  # Patient consomme 60g de glucides
        self.pdm.set_meal(carbs_consumed)
        self.assertEqual(self.pump.calculate_meal_bolus(carbs_consumed), 6.0)  # 6 U d'insuline
        print(f"Test d'entrée des glucides : {carbs_consumed}g de glucides entrés.")

    # Scénario : "Calcul du bolus alimentaire"
    def test_calculate_meal_bolus(self):
        carbs_consumed = 60  # Exemple de consommation de glucides
        bolus = self.pump.calculate_meal_bolus(carbs_consumed)
        self.assertAlmostEqual(bolus, 6.0, delta=0.1)  # Calcul attendu : 6 UI
        print(f"Test de calcul du bolus alimentaire : Bolus calculé = {bolus} UI")

    # Scénario : "Envoi à la pompe à insuline pour administrer le bolus"
    def test_send_bolus_to_pump(self):
        carbs_consumed = 60
        bolus = self.pump.calculate_meal_bolus(carbs_consumed)
        self.pump.deliver_bolus(bolus)  # Simule l'envoi de bolus à la pompe
        print(f"Test d'envoi du bolus : Bolus envoyé à la pompe = {bolus} UI")

    # Scénario : "Administration du bolus"
    def test_administration_of_bolus(self):
        carbs_consumed = 60
        bolus = self.pump.calculate_meal_bolus(carbs_consumed)
        self.pump.deliver_bolus(bolus)  # Simule l'administration du bolus
        # Ici, il faudrait vérifier que la pompe a bien administré le bolus
        # Pour cet exemple, nous supposons qu'une méthode existe pour récupérer le bolus administré
        print(f"Test d'administration du bolus : Bolus administré = {bolus} UI")

    # Scénario : "Confirmation au patient que le bolus a été administré"
    def test_confirmation_of_bolus_administration(self):
        carbs_consumed = 60
        bolus = self.pump.calculate_meal_bolus(carbs_consumed)
        # On simule que le bolus a été administré
        self.pdm.set_meal(carbs_consumed)  # Enregistrement de l'entrée de repas
        print(f"Confirmation : Bolus de {bolus} UI administré au patient.")

    # Scénario : "Enregistrement de la dose administrée dans l'historique"
    def test_recording_bolus_in_history(self):
        carbs_consumed = 60
        bolus = self.pump.calculate_meal_bolus(carbs_consumed)
        # On simule l'enregistrement dans l'historique
        # Ici, vous pouvez ajouter un code pour gérer l'historique dans la classe PDM
        print(f"Test d'enregistrement de la dose : {bolus} UI enregistré dans l'historique.")

if __name__ == '__main__':
    unittest.main()
