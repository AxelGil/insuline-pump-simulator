from flask import Blueprint, request, jsonify
from .models.pump_config import PumpConfig
from .models.insulin_pump import InsulinPump
from .models.patient import Patient
from .models.cgm import CGM
from .models.closed_loop_controller import ClosedLoopController
from .models.simulator import Simulator

main = Blueprint('main', __name__)

# Initial setup for the pump, patient, CGM, controller, and simulator
basal_rates = [0.8, 0.6, 0.5]  # Example basal rates
config = PumpConfig(basal_rates, 10, 30, 10)
patient = Patient(120)
pump = InsulinPump(config, patient)  # Pass the patient object
cgm = CGM(5)
controller = ClosedLoopController(120, pump, cgm)
simulator = Simulator(patient, pump, cgm, controller)


@main.route('/simulation', methods=['GET'])
def run_simulation():
    """
    Runs the simulation for 24 hours and returns the results.
    """
    results = []
    for hour, glucose in simulator.run_simulation():
        results.append({'hour': hour, 'glucose': glucose})

    return jsonify(results), 200

@main.route('/config', methods=['POST'])
def configure_pump():
    """
    Configures the pump parameters via a POST request.
    """
    data = request.get_json()
    basal_rates = data.get('basal_rates')
    insulin_to_carb_ratio = data.get('insulin_to_carb_ratio')
    insulin_sensitivity_factor = data.get('insulin_sensitivity_factor')
    max_bolus = data.get('max_bolus')

    # Apply the new configuration
    config = PumpConfig(basal_rates, insulin_to_carb_ratio, insulin_sensitivity_factor, max_bolus)
    pump.apply_configuration(config)

    return jsonify({"message": "Configuration successfully applied."}), 200
