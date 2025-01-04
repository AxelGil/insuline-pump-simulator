import pytest
from unittest.mock import patch, MagicMock
from app.dexcom_follow_app import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test de la route racine."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the dexcom_follow Microservice!"

@patch("sqlite3.connect")
@patch("builtins.open")
def test_suivredonnee_normal(mock_open, mock_connect, client):
    """Test pour vérifier la récupération des taux basaux et l'exportation correcte dans un fichier."""

    # Mock de la base de données
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Mock des données renvoyées par la requête SQL
    mock_cursor.fetchall.return_value = [(1, 100), (1, 110), (1, 120)]  # Valeurs de taux basaux à exporter

    # Mock de la fonction open pour éviter la création réelle du fichier
    mock_file = MagicMock()
    mock_open.return_value = mock_file

    # Requête avec un user_id fictif
    response = client.get('/suivredonnee', json={"user_id": 1})
    
    # Vérifications
    assert response.status_code == 200
    assert response.json == [100, 110, 120]  # Vérifier que les taux sont correctement renvoyés
    mock_cursor.execute.assert_called_once_with("SELECT * FROM user_basal_rate WHERE id_user = ?", (1,))
    mock_conn.close.assert_called_once()

    # Vérifier que la fonction exportFile est appelée et que les données sont écrites dans le fichier
    mock_open.assert_called_once_with("basal_rates.txt", "w")


@patch("sqlite3.connect")
def test_suivredonnee_user_id_absent(mock_connect, client):
    """Test pour une requête sans user_id."""
    response = client.get('/suivredonnee', json={})
    assert response.status_code == 400  # Erreur car user_id est manquant dans request.json
    assert "user_id is required" in response.data.decode()

@patch("sqlite3.connect")
def test_suivredonnee_user_id_invalide(mock_connect, client):
    """Test pour un user_id invalide (aucune donnée trouvée)."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Mock de la base de données pour ne pas renvoyer de données
    mock_cursor.fetchall.return_value = []  # Pas de résultats
    
    response = client.get('/suivredonnee', json={"user_id": 999})  # User_id fictif
    assert response.status_code == 404  # Pas de données trouvées pour cet user_id
    assert "No basal rates found" in response.data.decode()

