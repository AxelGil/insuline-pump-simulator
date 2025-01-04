import pytest
from unittest.mock import patch, MagicMock
from app.dexcom_platform_app import app
from app.dexcom_platform_app import checkBasalRate

@pytest.fixture
def client():
    """Fixture pour le client de test Flask."""
    with app.test_client() as client:
        yield client

# Test de la route / pour vérifier que l'application est en ligne
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the dexcom_platform Microservice!"

# Test de la route /transmettre pour un taux glucose normal
@patch("requests.get")
@patch("requests.post")
def test_transmettre_normal(mock_post, mock_get, client):
    """Test pour un taux de glucose normal qui ne doit pas appeler l'alerte."""
    mock_response_clarity = MagicMock()
    mock_response_follow = MagicMock()
    mock_response_clarity.json.return_value = {"message": "Clarity response"}
    mock_response_follow.json.return_value = {"message": "Follow response"}
    mock_get.return_value = mock_response_clarity
    mock_get.return_value = mock_response_follow

    mock_post.return_value = MagicMock(status_code=200)

    payload = {"taux_glucose": 100, "user_id": 1}
    response = client.post('/transmettre', json=payload)

    assert response.status_code == 200
    assert "responseClarity" in response.json
    assert "responseFollow" in response.json

    mock_get.assert_any_call("http://127.0.0.1:5002/analyser", json=payload)
    mock_get.assert_any_call("http://127.0.0.1:5003/suivredonnee", json=payload)

    mock_post.assert_not_called()  # L'alerte ne doit pas être envoyée


# Test de la route /transmettre pour un taux de glucose trop bas
@patch("requests.get")
@patch("requests.post")
def test_transmettre_taux_basal_bas(mock_post, mock_get, client):
    """Test pour un taux de glucose trop bas, qui devrait appeler l'alerte."""
    
    mock_response_clarity = MagicMock()
    mock_response_follow = MagicMock()
    mock_response_clarity.json.return_value = {"message": "Clarity response"}
    mock_response_follow.json.return_value = {"message": "Follow response"}
    mock_get.return_value = mock_response_clarity
    mock_get.return_value = mock_response_follow
    
    mock_post.return_value = MagicMock(status_code=200)
    
    payload = {"taux_glucose": 60, "user_id": 1}
    response = client.post('/transmettre', json=payload)
    
    assert response.status_code == 200
    assert "responseClarity" in response.json
    assert "responseFollow" in response.json
    mock_post.assert_called_once_with("http://127.0.0.1:5006/alerte", json={"alerte": "Le taux glycémique est trop bas"})

# Test de la route /transmettre pour un taux de glucose trop haut
@patch("requests.get")
@patch("requests.post")
def test_transmettre_taux_basal_haut(mock_post, mock_get, client):
    """Test pour un taux de glucose trop haut, qui devrait appeler l'alerte."""
    
    mock_response_clarity = MagicMock()
    mock_response_follow = MagicMock()
    mock_response_clarity.json.return_value = {"message": "Clarity response"}
    mock_response_follow.json.return_value = {"message": "Follow response"}
    mock_get.return_value = mock_response_clarity
    mock_get.return_value = mock_response_follow
    
    mock_post.return_value = MagicMock(status_code=200)
    
    payload = {"taux_glucose": 200, "user_id": 1}
    response = client.post('/transmettre', json=payload)
    
    assert response.status_code == 200
    assert "responseClarity" in response.json
    assert "responseFollow" in response.json
    mock_post.assert_called_once_with("http://127.0.0.1:5006/alerte", json={"alerte": "Le taux glycémique est trop haut"})

# Test de la fonction checkBasalRate pour un taux de glucose normal
def test_checkBasalRate_normal():
    result = checkBasalRate(100)
    assert result is None

# Test de la fonction checkBasalRate pour un taux de glucose trop bas
def test_checkBasalRate_bas():
    result = checkBasalRate(60)
    assert result == "Le taux glycémique est trop bas"

# Test de la fonction checkBasalRate pour un taux de glucose trop haut
def test_checkBasalRate_haut():
    result = checkBasalRate(200)
    assert result == "Le taux glycémique est trop haut"

# Test d'un taux de glucose absent dans la requête
def test_transmettre_without_taux_glucose(client):
    payload = {"user_id": 1}
    response = client.post('/transmettre', json=payload)
    assert response.status_code == 400  # On s'attend à une erreur car taux_glucose est manquant

# Test d'un user_id absent dans la requête
def test_transmettre_without_user_id(client):
    payload = {"taux_glucose": 100}
    response = client.post('/transmettre', json=payload)
    assert response.status_code == 400  # On s'attend à une erreur car user_id est manquant
