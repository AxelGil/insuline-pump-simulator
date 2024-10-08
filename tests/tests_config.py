import unittest
from app import create_app

class TestPumpConfig(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_configure_basal_rates(self):
        response = self.client.post('/config/basal_rates', json={
            'basal_rates': [0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Basal rates configured successfully.', response.get_json()['message'])
        self.assertEqual(response.get_json()['basal_rates'], [0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8])

    def test_configure_icr(self):
        response = self.client.post('/config/insulin_to_carb_ratio', json={
            'insulin_to_carb_ratio': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Insulin-to-carb ratio configured successfully.', response.get_json()['message'])
        self.assertEqual(response.get_json()['insulin_to_carb_ratio'], 10)

    def test_configure_isf(self):
        response = self.client.post('/config/insulin_sensitivity_factor', json={
            'insulin_sensitivity_factor': 30
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Insulin sensitivity factor configured successfully.', response.get_json()['message'])
        self.assertEqual(response.get_json()['insulin_sensitivity_factor'], 30)

    def test_configure_max_bolus(self):
        response = self.client.post('/config/max_bolus', json={
            'max_bolus': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Max bolus configured successfully.', response.get_json()['message'])
        self.assertEqual(response.get_json()['max_bolus'], 10)

    def test_configure_custom_mode(self):
        response = self.client.post('/config/custom_mode', json={
            'mode_name': 'night',
            'parameters': {
                'basal_rate': 0.5,
                'isf': 20,
                'icr': 8
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Custom mode 'night' configured successfully.", response.get_json()['message'])
        self.assertEqual(response.get_json()['mode']['name'], 'night')
        self.assertEqual(response.get_json()['mode']['parameters'], {
            'basal_rate': 0.5,
            'isf': 20,
            'icr': 8
        })

if __name__ == '__main__':
    unittest.main()
