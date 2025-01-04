import requests
import pytest
from unittest.mock import patch, MagicMock
import json
from app.cgm_app import app, transmettre_a_la_pompe, transmettre_recepteur_dedie

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the cgm_app Microservice!"

@patch("sqlite3.connect")
@patch("random.randint", return_value=120)
def test_mesurer_success(mock_randint, mock_connect, client):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    with patch("app.cgm_app.transmettre_a_la_pompe", return_value={"status": "success"}) as mock_pompe, \
         patch("app.cgm_app.transmettre_recepteur_dedie", return_value={"status": "success"}) as mock_recepteur:
        
        response = client.get("/mesurer?user_id=1")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "taux_glucose" in data
        assert "pomp_response" in data

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_pompe.assert_called_once_with(120, "http://127.0.0.1:5005")
        mock_recepteur.assert_called_once_with(120, 1)

def test_mesurer_missing_user_id(client):
    response = client.get("/mesurer")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Identifiant is missing"

def test_mesurer_invalid_user_id(client):
    response = client.get("/mesurer?user_id=abc")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Identifiant must be an integer"

@patch("requests.post")
def test_transmettre_a_la_pompe_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    result = transmettre_a_la_pompe(120, "http://127.0.0.1:5005")

    assert result == {"status": "success"}
    mock_post.assert_called_once_with("http://127.0.0.1:5005/ajuster", json={"taux_glucose": 120})

@patch("requests.post")
def test_transmettre_a_la_pompe_error(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("Error")

    result = transmettre_a_la_pompe(120, "http://127.0.0.1:5005")

    assert "error" in result

@patch("requests.post")
def test_transmettre_recepteur_dedie_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    result = transmettre_recepteur_dedie(120, 1)

    assert result == {"status": "success"}
    mock_post.assert_called_once_with("http://127.0.0.1:5006/transmettre", json={"taux_glucose": 120, "user_id": 1})

@patch("requests.post")
def test_transmettre_recepteur_dedie_error(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("Error")

    result = transmettre_recepteur_dedie(120, 1)

    assert "error" in result