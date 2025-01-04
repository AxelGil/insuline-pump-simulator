import pytest
from unittest.mock import patch, MagicMock
from app.dexcom_clarity_app import app  # Adapter l'import selon l'arborescence

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test de la route racine."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the DexCom Clarity Microservice!"

@patch("sqlite3.connect")
def test_analyser_taux_basal_normal(mock_connect, client):
    """Test pour un taux basal moyen normal."""
    # Mock de la base de données
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Mock des données renvoyées par la requête SQL
    mock_cursor.fetchall.return_value = [(1, 100), (1, 110), (1, 120)]  # Moyenne = 110
    
    # Requête avec un user_id fictif
    response = client.get('/analyser', json={"user_id": 1})
    
    # Vérifications
    assert response.status_code == 200
    assert "la moyenne de taux glycémique est normal" in response.data.decode()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM user_basal_rate WHERE id_user = ?", (1,))
    mock_conn.close.assert_called_once()

@patch("sqlite3.connect")
def test_analyser_taux_basal_trop_bas(mock_connect, client):
    """Test pour un taux basal moyen trop bas."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    mock_cursor.fetchall.return_value = [(1, 60), (1, 65), (1, 70)]  # Moyenne = 65
    
    response = client.get('/analyser', json={"user_id": 1})
    
    assert response.status_code == 200
    assert "la moyenne de taux glycémique est trop bas" in response.data.decode()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM user_basal_rate WHERE id_user = ?", (1,))
    mock_conn.close.assert_called_once()

@patch("sqlite3.connect")
def test_analyser_taux_basal_trop_haut(mock_connect, client):
    """Test pour un taux basal moyen trop haut."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    mock_cursor.fetchall.return_value = [(1, 190), (1, 200), (1, 210)]  # Moyenne = 200
    
    response = client.get('/analyser', json={"user_id": 1})
    
    assert response.status_code == 200
    assert "la moyenne de taux glycémique est trop haut" in response.data.decode()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM user_basal_rate WHERE id_user = ?", (1,))
    mock_conn.close.assert_called_once()

@patch("sqlite3.connect")
def test_analyser_user_id_absent(mock_connect, client):
    """Test pour une requête sans user_id."""
    response = client.get('/analyser', json={})
    assert response.status_code == 500  # Erreur car user_id manquant dans request.json