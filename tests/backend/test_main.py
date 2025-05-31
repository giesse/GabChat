import pytest
from unittest.mock import patch
# Import auth for verify_id_token and its exceptions like InvalidIdTokenError
from firebase_admin import auth 
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_verify_token_valid(client):
    with patch('firebase_admin.auth.verify_id_token') as mock_verify_id_token:
        mock_verify_id_token.return_value = {'uid': 'test_uid'}

        response = client.post('/verify-token', json={'token': 'valid_token'})
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['uid'] == 'test_uid'
        mock_verify_id_token.assert_called_once_with('valid_token')

def test_verify_token_invalid(client):
    with patch('firebase_admin.auth.verify_id_token') as mock_verify_id_token:
        # Raising a specific error that inherits from auth.AuthError
        mock_verify_id_token.side_effect = auth.InvalidIdTokenError("Invalid ID token.")

        response = client.post('/verify-token', json={'token': 'invalid_token'})
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid token' 
        assert 'details' in json_data # main.py includes details from the exception str(e)
        mock_verify_id_token.assert_called_once_with('invalid_token')

def test_verify_token_no_token(client):
    response = client.post('/verify-token', json={})
    
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'No token provided'

# Placeholder for future tests related to API key management
# def test_store_api_key_authenticated_user(client):
#     # TODO: Implement this test when API key storage is ready
#     pass

# def test_retrieve_api_key_authenticated_user(client):
#     # TODO: Implement this test when API key storage is ready
#     pass

# def test_api_key_unauthenticated(client):
#     # TODO: Test storing/retrieving API keys without authentication
#     pass
