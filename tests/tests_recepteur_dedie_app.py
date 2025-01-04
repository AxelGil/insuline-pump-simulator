import pytest
from flask import Flask, request
from flask.testing import FlaskClient
from unittest.mock import patch
import requests

# Créez l'application Flask pour les tests
@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Welcome to the pompe_insuline Microservice!"

    @app.route('/transmettre', methods=['POST'])
    def transmettre():
        taux_glucose = request.json.get("taux_glucose")
        addicherDonnées(taux_glucose)
        return transmettre_dexcom_platform(taux_glucose, request.json.get("user_id"))
      
    def transmettre_dexcom_platform(taux_glucose, user_id):
        payload = {"taux_glucose": taux_glucose, "user_id": user_id}
        try:
            response = requests.post("http://127.0.0.1:5004/transmettre", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def addicherDonnées(taux_glucose):
        print(f"(afficher sur recepteur dedie) Le taux de glucose est de {taux_glucose}")
        
    @app.route('/alerte', methods=['POST'])
    def alerte():
        alerte = request.json.get("alerte")
        print(f"Alerte reçue : {alerte}")
        return f"Alerte reçue : {alerte}"

    yield app

@pytest.fixture
def client(app: Flask):
    """Fixture pour créer un client de test Flask."""
    return app.test_client()

# Test de la route /transmettre avec un taux de glucose et user_id corrects
@patch('requests.post')
def test_transmettre(mock_post, client: FlaskClient):
    taux_glucose = 120
    user_id = 1
    mock_response = {"status": "success", "message": "Data transmitted successfully"}
    
    # Simuler la réponse de l'API Dexcom
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.status_code = 200

    payload = {"taux_glucose": taux_glucose, "user_id": user_id}
    response = client.post('/transmettre', json=payload)

    # Vérification de la réponse de l'API
    assert response.status_code == 200
    assert response.json == mock_response
    
    # Vérifier que la méthode requests.post a bien été appelée
    mock_post.assert_called_once_with("http://127.0.0.1:5004/transmettre", json=payload)

# Test de la route /alerte
def test_alerte(client: FlaskClient):
    alerte = {"alerte": "Le taux glycémique est trop bas"}
    response = client.post('/alerte', json=alerte)
    
    assert response.status_code == 200
    assert "Alerte reçue" in response.data.decode()
    assert "Le taux glycémique est trop bas" in response.data.decode()
