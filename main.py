import os
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, send_file, request, jsonify

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate("firebase-service-account-key.json")
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/verify-token", methods=["POST"])
def verify_token():
    id_token = request.json.get('token')
    if not id_token:
        return jsonify({"error": "No token provided"}), 400
    
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({"status": "success", "uid": uid}), 200
    # Catching the specific InvalidIdTokenError from firebase_admin.auth
    except auth.InvalidIdTokenError as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401
    # It might be good to also catch other specific auth errors if they are relevant
    # For example, if a token is expired, it might raise a different specific error.
    # For now, InvalidIdTokenError is what the test simulates.
    except Exception as e:
        # Catch any other unexpected errors during token verification
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
