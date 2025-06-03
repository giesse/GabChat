import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin.exceptions import FirebaseError
from flask import Flask, send_file, request, jsonify
from functools import wraps

# Global variables for Firebase app and Firestore client
fb_app = None
db = None

def initialize_firebase():
    global fb_app, db
    in_emulator_mode = bool(os.getenv("FIREBASE_AUTH_EMULATOR_HOST") or os.getenv("FIRESTORE_EMULATOR_HOST"))
    try:
        if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
            fb_app = firebase_admin.get_app()
            print(f"Using existing Firebase app: {fb_app.name}")
        else:
            print("No default Firebase app found, attempting to initialize.")
            try:
                cred = credentials.Certificate("firebase-service-account-key.json")
                fb_app = firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized with service account key.")
            except FileNotFoundError:
                if in_emulator_mode:
                    fb_app = firebase_admin.initialize_app()
                    print("Firebase Admin SDK initialized for emulator without service account key.")
                else:
                    print("Firebase Admin SDK NOT initialized (credentials not found, not emulator mode).")
                    fb_app = None 
            except Exception as e_init:
                print(f"Error during Firebase Admin SDK initialize_app: {e_init}")
                fb_app = None 
        if fb_app:
            db = firestore.client(app=fb_app)
            print(f"Firestore client configured for app: {fb_app.name}, Project: {db.project}")
        else:
            db = None 
            print("Firestore client NOT configured because Firebase App is not available.")
    except Exception as e:
        print(f"General error in initialize_firebase: {e}")
        fb_app = None
        db = None

app = Flask(__name__, static_folder='src', static_url_path='')
initialize_firebase()

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        id_token = None
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split('Bearer ')[1]
        if not id_token:
            return jsonify({"error": "Unauthorized", "message": "Authentication token is missing."}), 401
        try:
            decoded_token = auth.verify_id_token(id_token)
            current_user_uid = decoded_token['uid']
        except FirebaseError as e: 
            return jsonify({"error": "Unauthorized", "message": f"Token verification failed: {str(e)}"}), 401
        except Exception as e: 
            return jsonify({"error": "Unauthorized", "message": f"An unexpected error occurred during token verification: {str(e)}"}), 401
        return f(current_user_uid, *args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/verify-token", methods=["POST"])
def verify_token():
    auth_header = request.headers.get('Authorization')
    id_token = None
    if auth_header and auth_header.startswith('Bearer '):
        id_token = auth_header.split('Bearer ')[1]
    if not id_token and request.is_json:
        id_token = request.json.get('token')
    if not id_token:
        return jsonify({"error": "No token provided"}), 400
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({"status": "success", "uid": uid}), 200
    except FirebaseError as e: 
        return jsonify({"error": "Invalid token", "details": str(e)}), 401
    except Exception as e: 
        return jsonify({"error": "An unexpected error occurred during token verification", "details": str(e)}), 500

@app.route("/api/gemini-key", methods=["POST"])
@token_required
def store_gemini_key(current_user_uid):
    if not db:
        return jsonify({"error": "Firestore client not available. DB is None."}), 500
    data = request.get_json()
    if not data or 'api_key' not in data:
        return jsonify({"error": "API key is missing in request body."}), 400
    api_key = data['api_key']
    if not isinstance(api_key, str) or not api_key.strip():
        return jsonify({"error": "API key must be a non-empty string."}), 400
    try:
        doc_ref = db.collection('user_gemini_keys').document(current_user_uid)
        doc_ref.set({'api_key': api_key})
        return jsonify({"status": "success", "message": "API key stored successfully."}), 200
    except FirebaseError as e: 
        return jsonify({"error": "Failed to store API key in Firestore", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to store API key", "details": str(e)}), 500

@app.route("/api/gemini-key", methods=["GET"])
@token_required
def get_gemini_key(current_user_uid):
    if not db:
        return jsonify({"error": "Firestore client not available. DB is None."}), 500
    try:
        doc_ref = db.collection('user_gemini_keys').document(current_user_uid)
        doc = doc_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "API key not found."}), 404
    except FirebaseError as e: 
        return jsonify({"error": "Failed to retrieve API key from Firestore", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to retrieve API key", "details": str(e)}), 500

@app.route("/api/gemini-key", methods=["DELETE"])
@token_required
def delete_gemini_key(current_user_uid):
    if not db:
        return jsonify({"error": "Firestore client not available. DB is None."}), 500
    try:
        doc_ref = db.collection('user_gemini_keys').document(current_user_uid)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return jsonify({"status": "success", "message": "API key deleted successfully."}), 200
        else:
            return jsonify({"error": "API key not found to delete."}), 404
    except FirebaseError as e: 
        return jsonify({"error": "Failed to delete API key from Firestore", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to delete API key", "details": str(e)}), 500

def run_flask_app():
    if os.getenv("FIREBASE_EMULATORS_EXEC_MODE") == "true":
      print("Running with Firebase Emulators (exec mode) - data will persist if configured.")
    elif os.getenv("FIRESTORE_EMULATOR_HOST"):
      print(f"Running with Firestore emulator at {os.getenv('FIRESTORE_EMULATOR_HOST')}")
    
    port = int(os.environ.get('PORT', 8080))
    # Respect FLASK_DEBUG environment variable for debug mode
    flask_debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=flask_debug)

if __name__ == "__main__":
    run_flask_app()
