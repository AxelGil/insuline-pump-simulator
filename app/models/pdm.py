class PDM:
    def __init__(self, pump, target_glucose, controller, config):
        self.pump = pump
        self.target_glucose = target_glucose
        self.controller = controller
        self.config = config

    def set_meal(self, carbs):
        # Calculate the required bolus based on the consumed carbs and the patient's insulin sensitivity
        bolus = self.controller.calculate_bolus(carbs)

        # Deliver the bolus
        self.pump.deliver_bolus(bolus)

    def set_target_glucose(self, target):
        self.target_glucose = target
        self.controller.update_target_glucose(target)

    def apply_new_config(self, config):
        self.config = config
        self.pump.apply_config(config)

    def add_alarm(self, alarm):
        # Add the alarm to the PDM's alarm list
        self.alarms.append(alarm)

    def view_history(self):
        # Retrieve and display the history of glucose levels, insulin doses, and alarms
        history = self.pump.get_history()
        print(history)

    def set_mode(self, mode, config):
        # Set the PDM's mode (e.g., "day", "night") and apply the corresponding configuration
        self.mode = mode
        self.apply_new_config(config)