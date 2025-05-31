import pytest
import os
import requests # For interacting with emulator REST API
from unittest.mock import patch
from firebase_admin import auth
from main import app # Assuming your Flask app is named 'app' in main.py

# Configuration for Firebase Auth Emulator
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "gabchat-e1851")
FIREBASE_AUTH_EMULATOR_HOST = "127.0.0.1:9099"
# This is a generic API key that often works with emulators for REST calls.
# It might not be strictly necessary for all emulator endpoints, but it's good practice for :signUp.
EMULATOR_API_KEY = "AIzaSyA0...emulator_key" # Placeholder, can be any string for emulator

@pytest.fixture(scope="session")
def client_with_emulator_config():
    original_emulator_host = os.environ.get("FIREBASE_AUTH_EMULATOR_HOST")
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = FIREBASE_AUTH_EMULATOR_HOST
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
    if original_emulator_host is None:
        del os.environ["FIREBASE_AUTH_EMULATOR_HOST"]
    else:
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = original_emulator_host

@pytest.fixture
def client(client_with_emulator_config):
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

def create_user_and_get_token_emulator(email, password):
    # Using accounts:signUp endpoint, which is standard for Firebase Auth REST API
    create_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:signUp?key={EMULATOR_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        resp = requests.post(create_user_url, json=payload)
        resp.raise_for_status() # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        user_data = resp.json()
        return user_data['idToken'], user_data['localId']
    except requests.exceptions.RequestException as e:
        print(f"Error creating user in emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")
        raise

def delete_emulator_user(local_id):
    # Using accounts:delete endpoint
    delete_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:delete?key={EMULATOR_API_KEY}"
    payload = {"localId": local_id}
    try:
        resp = requests.post(delete_user_url, json=payload)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log error but don't re-raise during cleanup
        print(f"Error deleting user {local_id} from emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")

@pytest.mark.emulator
def test_verify_token_with_emulator(client):
    test_email = f"testuser.emulator.{os.urandom(4).hex()}@example.com" # Unique email to avoid collisions
    test_password = "securePassword123"
    id_token = None
    local_id = None

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
