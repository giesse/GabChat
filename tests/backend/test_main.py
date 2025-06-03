import pytest
import os
import requests
from unittest.mock import patch
import firebase_admin # Import firebase_admin itself
from firebase_admin import auth, firestore 
from main import app, initialize_firebase as initialize_firebase_in_main # Import app and the initializer

# Configuration for Firebase Emulators
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "gabchat-e1851")
FIREBASE_AUTH_EMULATOR_HOST = "127.0.0.1:9099"
FIRESTORE_EMULATOR_HOST = "127.0.0.1:8080" # As per firebase.json
EMULATOR_API_KEY = "AIzaSyA0...emulator_key"

@pytest.fixture(scope="session")
def client_with_emulator_config():
    original_auth_emulator_host = os.environ.get("FIREBASE_AUTH_EMULATOR_HOST")
    original_firestore_emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")

    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = FIREBASE_AUTH_EMULATOR_HOST
    os.environ["FIRESTORE_EMULATOR_HOST"] = FIRESTORE_EMULATOR_HOST

    # If a default Firebase app already exists (from main.py's initial import),
    # delete it so that initialize_firebase_in_main() can create a new one
    # that correctly uses the emulator environment variables.
    if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
        print(f"Deleting existing Firebase app: {firebase_admin.get_app().name} before re-initializing for tests.")
        firebase_admin.delete_app(firebase_admin.get_app())
    
    # Re-initialize Firebase within main.py's context *after* env vars are set
    initialize_firebase_in_main()
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
    # Teardown: Restore original environment variables
    if original_auth_emulator_host is None:
        if "FIREBASE_AUTH_EMULATOR_HOST" in os.environ:
            del os.environ["FIREBASE_AUTH_EMULATOR_HOST"]
    else:
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = original_auth_emulator_host
    
    if original_firestore_emulator_host is None:
        if "FIRESTORE_EMULATOR_HOST" in os.environ:
            del os.environ["FIRESTORE_EMULATOR_HOST"]
    else:
        os.environ["FIRESTORE_EMULATOR_HOST"] = original_firestore_emulator_host
    
    # Clean up the Firebase app used for testing, if it exists
    if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
         print(f"Deleting Firebase app: {firebase_admin.get_app().name} after tests.")
         firebase_admin.delete_app(firebase_admin.get_app())

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
    # Patching auth.verify_id_token which is used inside main.py's verify_token route
    with patch('main.auth.verify_id_token') as mock_verify_id_token: 
        # We also need to import FirebaseError from firebase_admin.exceptions for this mock
        from firebase_admin.exceptions import FirebaseError
        mock_verify_id_token.side_effect = FirebaseError(code="auth/invalid-id-token", message="Invalid mock ID token.")
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
    create_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:signUp?key={EMULATOR_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        resp = requests.post(create_user_url, json=payload)
        resp.raise_for_status()
        user_data = resp.json()
        return user_data['idToken'], user_data['localId']
    except requests.exceptions.RequestException as e:
        print(f"Error creating user in emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")
        raise

def delete_emulator_user(local_id):
    # This function needs an ID token of an admin or the user themselves for a real Firebase project.
    # For the emulator, it might require a specific setup or sometimes just works with a generic key if unprotected.
    # The error "MISSING_ID_TOKEN" suggests it needs some form of auth even for the emulator's delete endpoint.
    # For simplicity in tests, we often rely on the Auth emulator resetting or not needing specific user deletion if tests are isolated.
    # However, if user deletion is critical for test logic, this function might need adjustment or an admin token for the emulator.
    delete_user_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:delete?key={EMULATOR_API_KEY}"
    payload = {"localId": local_id} # This is correct for deleting by localId if the endpoint is unprotected or if EMULATOR_API_KEY is sufficient.
                                  # For `MISSING_ID_TOKEN` it implies the user's own ID Token might be needed in an `idToken` field in the payload for this emulator version.
    try:
        print(f"Attempting to delete user {local_id} from emulator.")
        resp = requests.post(delete_user_url, json=payload) # Changed from data= to json= for consistency
        resp.raise_for_status()
        print(f"Successfully deleted user {local_id} from emulator.")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting user {local_id} from emulator: {e}. Response: {resp.text if 'resp' in locals() else 'N/A'}")
        # Not re-raising, as it's a cleanup step.

@pytest.mark.emulator
def test_verify_token_with_emulator(client):
    test_email = f"testuser.emulator.{os.urandom(4).hex()}@example.com"
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

TEST_GEMINI_API_KEY = "test_gemini_api_key_firestore_123"

@pytest.mark.emulator
def test_store_gemini_key_authenticated(client):
    test_email = f"gemini_user_store.{os.urandom(4).hex()}@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None
    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        headers = {'Authorization': f'Bearer {id_token}', 'Content-Type': 'application/json'}
        response_post = client.post('/api/gemini-key', headers=headers, json={'api_key': TEST_GEMINI_API_KEY})
        assert response_post.status_code == 200, response_post.get_data(as_text=True)
        assert response_post.get_json() == {'status': 'success', 'message': 'API key stored successfully.'}
    finally:
        if local_id:
            if id_token:
                 headers_cleanup = {'Authorization': f'Bearer {id_token}'}
                 client.delete('/api/gemini-key', headers=headers_cleanup) 
            delete_emulator_user(local_id)

@pytest.mark.emulator
def test_store_gemini_key_unauthenticated(client):
    response = client.post('/api/gemini-key', json={'api_key': TEST_GEMINI_API_KEY})
    assert response.status_code == 401, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data['error'] == 'Unauthorized' 
    assert "Authentication token is missing" in json_data.get('message', '')

@pytest.mark.emulator
def test_get_gemini_key_authenticated(client):
    test_email = f"gemini_user_get.{os.urandom(4).hex()}@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None
    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        headers = {'Authorization': f'Bearer {id_token}', 'Content-Type': 'application/json'}
        client.post('/api/gemini-key', headers=headers, json={'api_key': TEST_GEMINI_API_KEY}) 
        response_get = client.get('/api/gemini-key', headers=headers)
        assert response_get.status_code == 200, response_get.get_data(as_text=True)
        assert response_get.get_json() == {'has_key': True}
    finally:
        if local_id:
            if id_token:
                 headers_cleanup = {'Authorization': f'Bearer {id_token}'}
                 client.delete('/api/gemini-key', headers=headers_cleanup)
            delete_emulator_user(local_id)

@pytest.mark.emulator
def test_get_gemini_key_unauthenticated(client):
    response = client.get('/api/gemini-key')
    assert response.status_code == 401, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data['error'] == 'Unauthorized'
    assert "Authentication token is missing" in json_data.get('message', '')

@pytest.mark.emulator
def test_get_gemini_key_no_key_stored(client):
    test_email = f"gemini_user_no_key.{os.urandom(4).hex()}@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None
    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        headers = {'Authorization': f'Bearer {id_token}'}
        response_get = client.get('/api/gemini-key', headers=headers)
        assert response_get.status_code == 200, response_get.get_data(as_text=True)
        assert response_get.get_json() == {'has_key': False}
    finally:
        if local_id:
            delete_emulator_user(local_id)

@pytest.mark.emulator
def test_delete_gemini_key_authenticated(client):
    test_email = f"gemini_user_delete.{os.urandom(4).hex()}@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None
    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        headers = {'Authorization': f'Bearer {id_token}', 'Content-Type': 'application/json'}
        client.post('/api/gemini-key', headers=headers, json={'api_key': TEST_GEMINI_API_KEY}) 
        response_delete = client.delete('/api/gemini-key', headers=headers)
        assert response_delete.status_code == 200, response_delete.get_data(as_text=True)
        assert response_delete.get_json() == {'status': 'success', 'message': 'API key deleted successfully.'}
        response_get = client.get('/api/gemini-key', headers=headers) 
        assert response_get.status_code == 200, response_get.get_data(as_text=True)
        assert response_get.get_json() == {'has_key': False}
    finally:
        if local_id:
            delete_emulator_user(local_id)

@pytest.mark.emulator
def test_delete_gemini_key_unauthenticated(client):
    response = client.delete('/api/gemini-key')
    assert response.status_code == 401, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data['error'] == 'Unauthorized'
    assert "Authentication token is missing" in json_data.get('message', '')

@pytest.mark.emulator
def test_delete_gemini_key_no_key_to_delete(client):
    test_email = f"gemini_user_del_no_key.{os.urandom(4).hex()}@example.com"
    test_password = "securePassword123"
    id_token = None
    local_id = None
    try:
        id_token, local_id = create_user_and_get_token_emulator(test_email, test_password)
        headers = {'Authorization': f'Bearer {id_token}'}
        response_delete = client.delete('/api/gemini-key', headers=headers)
        assert response_delete.status_code == 404, response_delete.get_data(as_text=True)
        assert response_delete.get_json() == {'error': 'API key not found to delete.'}
    finally:
        if local_id:
            delete_emulator_user(local_id)
