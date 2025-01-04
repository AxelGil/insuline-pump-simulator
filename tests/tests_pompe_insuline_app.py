import pytest
from flask import Flask, jsonify, request
from flask.testing import FlaskClient
from unittest.mock import patch
from app.pompe_insuline_app import PompeInsuline

# Créez l'application Flask pour les tests
@pytest.fixture
def app():
    app = Flask(__name__)

    # Définition de la route pour ajuster l'insuline
    @app.route('/ajuster', methods=['POST'])
    def ajuster():
        data = request.json
        taux_glucose = data.get("taux_glucose")
        if taux_glucose is None:
            return jsonify({"error": "Taux de glucose manquant"}), 400

        action = PompeInsuline.ajusterTraitementAutomatique(taux_glucose)
        
        return jsonify({
            "taux_glucose": taux_glucose,
            "action": action
        })
    
    yield app

@pytest.fixture
def client(app: Flask):
    """Fixture pour créer un client de test Flask."""
    return app.test_client()

# Test de l'API quand le taux de glucose est manquant
def test_ajuster_without_taux_glucose(client: FlaskClient):
    response = client.post('/ajuster', json={})
    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Taux de glucose manquant"

# Test de l'API avec un taux de glucose normal
@patch.object(PompeInsuline, 'ajusterTraitementAutomatique')
def test_ajuster_normal(mock_ajuster, client: FlaskClient):
    taux_glucose = 100
    expected_action = "maintenir"  # Supposons que pour un taux de glucose de 100, l'action est "maintenir"

    # Simuler la méthode ajusterTraitementAutomatique
    mock_ajuster.return_value = expected_action

    response = client.post('/ajuster', json={"taux_glucose": taux_glucose})
    
    assert response.status_code == 200
    assert response.json["taux_glucose"] == taux_glucose
    assert response.json["action"] == expected_action

# Test de l'API avec un taux de glucose trop bas
@patch.object(PompeInsuline, 'ajusterTraitementAutomatique')
def test_ajuster_below_threshold(mock_ajuster, client: FlaskClient):
    taux_glucose = 50
    expected_action = "augmenter insuline"  # Supposons que pour un taux bas, l'action soit "augmenter insuline"
    
    # Simuler la méthode ajusterTraitementAutomatique
    mock_ajuster.return_value = expected_action

    response = client.post('/ajuster', json={"taux_glucose": taux_glucose})
    
    assert response.status_code == 200
    assert response.json["taux_glucose"] == taux_glucose
    assert response.json["action"] == expected_action

# Test de l'API avec un taux de glucose trop élevé
@patch.object(PompeInsuline, 'ajusterTraitementAutomatique')
def test_ajuster_high_glucose(mock_ajuster, client: FlaskClient):
    taux_glucose = 200
    expected_action = "réduire insuline"  # Supposons que pour un taux élevé, l'action soit "réduire insuline"
    
    # Simuler la méthode ajusterTraitementAutomatique
    mock_ajuster.return_value = expected_action

    response = client.post('/ajuster', json={"taux_glucose": taux_glucose})
    
    assert response.status_code == 200
    assert response.json["taux_glucose"] == taux_glucose
    assert response.json["action"] == expected_action
