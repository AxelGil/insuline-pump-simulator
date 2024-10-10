# import unittest
# from app.models.pump_config import PumpConfig
# from app.models.insulin_pump import InsulinPump
# from app.models.closed_loop_controller import ClosedLoopController
# from app.models.cgm import CGM
# from app.models.patient import Patient
# from app.models.pdm import PDM


# class TestsUserStory6(unittest.TestCase):

#     def setUp(self):
#         # Configuration initiale de la pompe à insuline
#         self.config = PumpConfig(
#             basal_rates=[0.8, 0.6, 0.7], 
#             insulin_to_carb_ratio=10.0,  
#             min_sensitivity_factor=30.0, 
#             max_bolus=10.0, 
#             modes={"jour": {"basal_increase": 0.1}, "nuit": {"basal_decrease": 0.15}}
#         )

#         # Initialisation des objets nécessaires
#         self.patient = Patient(initial_glucose=120, carb_intake=60, sensitivity=5, insulin_sensitivity=2)
#         self.pump = InsulinPump(self.config)
#         self.cgm = CGM(measurement_interval=5)
#         self.controller = ClosedLoopController(target_glucose=100, insulin_pump=self.pump, cgm=self.cgm)
#         self.pdm = PDM(pump=self.pump, config=self.config, controller=self.controller, target_glucose=100)

#     # Scénario : "Accès à l'historique des données"
#     def test_access_to_data_history(self):
#         # Simuler des événements pour remplir l'historique
#         self.pdm.set_meal(60)  # 60g de glucides
#         self.pump.deliver_bolus(6.0)  # Bolus de 6 UI
#         self.patient.update_glucose(insulin=6.0, carbs=60)  # Mise à jour de la glycémie

#         # Affichage de l'historique (à implémenter dans la classe PDM)
#         history = self.pdm.view_history()
#         self.assertTrue(len(history) > 0, "L'historique devrait contenir des données après des événements.")
#         print("Test d'accès à l'historique des données réussi.")

#     # Scénario : "Affichage des données historiques dans un format lisible"
#     def test_display_of_data_history(self):
#         self.pdm.set_meal(60)  # 60g de glucides
#         self.pump.deliver_bolus(6.0)  # Bolus de 6 UI
#         self.patient.update_glucose(insulin=6.0, carbs=60)  # Mise à jour de la glycémie

#         # Vérifier que l'historique est affiché correctement
#         history = self.pdm.view_history()
#         for entry in history:
#             print(f"Date : {entry['date']}, Glycémie : {entry['glucose']} mg/dL, Insuline : {entry['insulin']} U, Repas : {entry['carbs']} g")
#         print("Test d'affichage des données historiques réussi.")

#     # Scénario : "Mise à jour de l'historique après chaque événement significatif"
#     def test_update_history_after_event(self):
#         initial_history_length = len(self.pdm.history)  # Longueur initiale de l'historique
#         self.pdm.set_meal(60)  # 60g de glucides
#         self.pump.deliver_bolus(6.0)  # Bolus de 6 UI
#         self.patient.update_glucose(insulin=6.0, carbs=60)  # Mise à jour de la glycémie
#         new_history_length = len(self.pdm.history)  # Longueur après les événements

#         self.assertGreater(new_history_length, initial_history_length, "L'historique devrait être mis à jour après un événement.")
#         print(f"Test de mise à jour de l'historique réussi : Longueur de l'historique mise à jour de {initial_history_length} à {new_history_length}.")

# if __name__ == '__main__':
#     unittest.main()
