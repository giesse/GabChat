import os
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, send_file, request, jsonify

# Initialize Firebase Admin SDK
try:
    # Attempt to load service account credentials if the file exists
    cred = credentials.Certificate("firebase-service-account-key.json")
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized with service account key.")
except FileNotFoundError:
    # If the service account key is not found, and we are likely in an emulator environment
    # The Admin SDK will auto-discover emulators if FIREBASE_AUTH_EMULATOR_HOST is set.
    if os.getenv("FIREBASE_AUTH_EMULATOR_HOST"):
        firebase_admin.initialize_app()
        print("Firebase Admin SDK initialized for emulator without service account key.")
    else:
        # Handle the case where neither service account nor emulator is configured
        print("Firebase Admin SDK NOT initialized. Service account key not found and FIREBASE_AUTH_EMULATOR_HOST not set.")
        # Depending on your app's needs, you might raise an error here or have a default behavior.
except Exception as e:
    print(f"An unexpected error occurred during Firebase Admin SDK initialization: {e}")


app = Flask(__name__, static_folder='src', static_url_path='')

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/verify-token", methods=["POST"])
def verify_token():
    # Check for Authorization header first (Bearer token)
    auth_header = request.headers.get('Authorization')
    id_token = None
    if auth_header and auth_header.startswith('Bearer '):
        id_token = auth_header.split('Bearer ')[1]
    
    # Fallback to checking JSON body if no Bearer token
    if not id_token and request.is_json:
        id_token = request.json.get('token')

    if not id_token:
        return jsonify({"error": "No token provided"}), 400
    
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({"status": "success", "uid": uid}), 200
    except auth.InvalidIdTokenError as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred during token verification", "details": str(e)}), 500

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
