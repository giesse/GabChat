import pytest
import os
import requests # For interacting with emulator REST API
from unittest.mock import patch
from firebase_admin import auth
from main import app # Assuming your Flask app is named 'app' in main.py

# Configuration for Firebase Auth Emulator (values from src/index.html)
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "gabchat-e1851")
FIREBASE_AUTH_EMULATOR_HOST = "localhost:9099" # From firebase.json
FIREBASE_API_KEY = "AIzaSyBRS6_fValVt0ZPtcLykcfcuZe2UYOEGHo" # apiKey from src/index.html

@pytest.fixture(scope="session") # Changed to session scope for efficiency if multiple tests use it
def client_with_emulator_config():
    # This fixture ensures the main app context (if it reads env vars at startup)
    # is aware of the emulator. It's good practice.
    original_emulator_host = os.environ.get("FIREBASE_AUTH_EMULATOR_HOST")
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = FIREBASE_AUTH_EMULATOR_HOST
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
    # Restore original environment variable state
    if original_emulator_host is None:
        del os.environ["FIREBASE_AUTH_EMULATOR_HOST"]
    else:
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = original_emulator_host

@pytest.fixture
def client(client_with_emulator_config): # Use the emulator-configured client for all tests by default
    yield client_with_emulator_config

# --- Mock Tests (existing tests) ---
def test_verify_token_valid_mock(client):
    with patch('firebase_admin.auth.verify_id_token') as mock_verify_id_token:
        mock_verify_id_token.return_value = {'uid': 'test_uid_mock'}
        response = client.post('/verify-token', json={'token': 'valid_mock_token'})
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['uid'] == 'test_uid_mock'
        mock_verify_id_token.assert_called_once_with('valid_mock_token')

def test_verify_token_invalid_mock(client):
    with patch('firebase_admin.auth.verify_id_token') as mock_verify_id_token:
        mock_verify_id_token.side_effect = auth.InvalidIdTokenError("Invalid mock ID token.")
        response = client.post('/verify-token', json={'token': 'invalid_mock_token'})
        assert response.status_code == 401
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid token'
        mock_verify_id_token.assert_called_once_with('invalid_mock_token')

def test_verify_token_no_token_mock(client):
    response = client.post('/verify-token', json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'No token provided'

# --- Emulator Test ---

# Helper function to create a user in the emulator and get an ID token
def create_user_and_get_token_emulator(email, password):
    create_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        resp = requests.post(create_user_url, json=payload)
        resp.raise_for_status()
        user_data = resp.json()
        return user_data['idToken'], user_data['localId']
    except requests.exceptions.RequestException as e:
        print(f"Error creating user in emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")
        raise

# Helper function to delete a user from the emulator
def delete_emulator_user(local_id):
    delete_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:delete?key={FIREBASE_API_KEY}"
    payload = {"localId": local_id}
    try:
        resp = requests.post(delete_user_url, json=payload)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error deleting user {local_id} from emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")
        # Not raising here as it's a cleanup step, but good to log

@pytest.mark.emulator
def test_verify_token_with_emulator(client): # client fixture already uses client_with_emulator_config
    test_email = "testuser.emulator@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None

    # Ensure emulators are running before this test
    # You might want to add a check here or rely on CI setup

    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        assert id_token is not None
        assert local_id is not None

        headers = {'Authorization': f'Bearer {id_token}'}
        response = client.post('/verify-token', headers=headers)

        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response is not None
        assert json_response['status'] == 'success'
        assert json_response['uid'] == local_id

    finally:
        if local_id:
            delete_emulator_user(local_id)

# To run only emulator tests: pytest -m emulator
# To run all tests: pytest

# Placeholder for future tests related to API key management
# def test_store_api_key_authenticated_user(client):
#     # TODO: Implement this test when API key storage is ready
#     pass
