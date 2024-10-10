import time
from app.models.cgm import CGM
from app.models.closed_loop_controller import ClosedLoopController
from app.models.insulin_pump import InsulinPump
from app.models.patient import Patient
from app.models.pump_config import PumpConfig


class InsulinPumpSimulator:
    def __init__(self, 
                 pump_config: PumpConfig, 
                 patient: Patient, 
                 insulin_pump: InsulinPump, 
                 cgm: CGM, 
                 closed_loop_controller: ClosedLoopController, 
                 simulation_duration):
        
        self.pump_config = pump_config
        self.patient = patient
        self.insulin_pump = insulin_pump
        self.cgm = cgm
        self.closed_loop_controller = closed_loop_controller
        self.simulation_duration = simulation_duration

    def run_simulation(self):
        for _ in range(self.simulation_duration):
            # Simuler le passage du temps
            time.sleep(1)  # Ajuster le pas de temps selon vos besoins

            # Mesurer la glycémie
            current_glucose = self.cgm.measure_glucose(self.patient)

            # Contrôle en boucle fermée
            self.closed_loop_controller.control_loop(self.patient, current_glucose)

            # Mettre à jour l'état du patient
            self.patient.update_state(current_glucose)

            # Enregistrer les données
            self.log_data(current_glucose, self.insulin_pump.last_bolus)


    def log_data(self, glucose, insulin_dose):
        self.data.append({
            "time": time.time(),
            "glucose": glucose,
            "insulin": insulin_dose
        })