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
    # You might want to handle this more gracefully in production
    # For now, we'll print the error and continue, 
    # but Firebase-dependent features won't work.

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
        # You can store user details or manage sessions here
        # For now, just return the UID
        return jsonify({"status": "success", "uid": uid}), 200
    except auth.FirebaseAuthException as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401
    except Exception as e:
        # Catch any other unexpected errors during token verification
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
