from flask import Blueprint, request, jsonify
from .models.pump_config import PumpConfig
from .models.insulin_pump import InsulinPump
from .models.patient import Patient
from .models.cgm import CGM
from .models.closed_loop_controller import ClosedLoopController
from .models.simulator import Simulator

main = Blueprint('main', __name__)

# Setup for the insulin pump simulator
config = PumpConfig()
patient = Patient(120)
pump = InsulinPump(config, patient)
cgm = CGM(5)
controller = ClosedLoopController(120, pump, cgm)
simulator = Simulator(patient, pump, cgm, controller)

@main.route('/config/basal_rates', methods=['POST'])
def configure_basal_rates():
    data = request.get_json()
    basal_rates = data.get('basal_rates')

    if len(basal_rates) != 24:
        return jsonify({"error": "Basal rates must have exactly 24 values (one for each hour)."}), 400

    config.basal_rates = basal_rates
    return jsonify({
        "message": "Basal rates configured successfully.",
        "basal_rates": config.basal_rates
    }), 200

@main.route('/config/insulin_to_carb_ratio', methods=['POST'])
def configure_icr():
    data = request.get_json()
    ratio = data.get('insulin_to_carb_ratio')

    config.insulin_to_carb_ratio = ratio
    return jsonify({
        "message": "Insulin-to-carb ratio configured successfully.",
        "insulin_to_carb_ratio": config.insulin_to_carb_ratio
    }), 200

@main.route('/config/insulin_sensitivity_factor', methods=['POST'])
def configure_isf():
    data = request.get_json()
    isf = data.get('insulin_sensitivity_factor')

    config.insulin_sensitivity_factor = isf
    return jsonify({
        "message": "Insulin sensitivity factor configured successfully.",
        "insulin_sensitivity_factor": config.insulin_sensitivity_factor
    }), 200

@main.route('/config/max_bolus', methods=['POST'])
def configure_max_bolus():
    data = request.get_json()
    max_bolus = data.get('max_bolus')

    config.max_bolus = max_bolus
    return jsonify({
        "message": "Max bolus configured successfully.",
        "max_bolus": config.max_bolus
    }), 200

@main.route('/config/custom_mode', methods=['POST'])
def configure_custom_mode():
    data = request.get_json()
    mode_name = data.get('mode_name')
    parameters = data.get('parameters')

    config.set_custom_mode(mode_name, parameters)
    return jsonify({
        "message": f"Custom mode '{mode_name}' configured successfully.",
        "mode": {
            "name": mode_name,
            "parameters": parameters
        }
    }), 200
