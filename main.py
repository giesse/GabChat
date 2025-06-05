import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin.exceptions import FirebaseError
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from functools import wraps
import google.generativeai as genai

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
CORS(app, resources={r"/api/*": {"origins": "*"}})
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
        return jsonify({"error": "Firestore client not available", "details": "DB is None."}), 500
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
        return jsonify({"error": "Firestore client not available", "details": "DB is None."}), 500
    try:
        doc_ref = db.collection('user_gemini_keys').document(current_user_uid)
        doc = doc_ref.get()
        if doc.exists:
            return jsonify({"has_key": True}), 200
        else:
            return jsonify({"has_key": False}), 200 
    except FirebaseError as e: 
        return jsonify({"error": "Failed to retrieve API key status from Firestore", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error retrieving API key status", "details": str(e)}), 500

@app.route("/api/gemini-key", methods=["DELETE"])
@token_required
def delete_gemini_key(current_user_uid):
    if not db:
        return jsonify({"error": "Firestore client not available", "details": "DB is None."}), 500
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
        return jsonify({"error": "Unexpected error deleting API key", "details": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
@token_required
def chat_with_gemini(current_user_uid):
    if not db:
        return jsonify({"error": "Firestore client not available", "details": "DB is None."}), 500

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Bad Request", "message": "Message is required."}), 400
    
    user_message = data['message']
    if not user_message.strip():
        return jsonify({"error": "Bad Request", "message": "Message cannot be empty."}), 400

    try:
        key_doc_ref = db.collection('user_gemini_keys').document(current_user_uid)
        key_doc = key_doc_ref.get()
        if not key_doc.exists:
            return jsonify({"error": "Configuration Error", "message": "Gemini API key not configured for this user. Please set it up in the settings."}), 400
        
        gemini_api_key = key_doc.to_dict().get('api_key')
        if not gemini_api_key:
            return jsonify({"error": "Configuration Error", "message": "Gemini API key is missing or invalid in the database."}), 500

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') 
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text}), 200

    except FirebaseError as e:
        return jsonify({"error": "Firestore Error", "message": f"Failed to retrieve Gemini API key: {str(e)}"}), 500
    except Exception as e:
        # This will catch errors from genai.configure, GenerativeModel, or generate_content
        # It's good practice to log the specific error `e` on the server for debugging.
        print(f"Error during Gemini API interaction: {e}") # Log for server-side debugging
        # Provide a more generic error to the client for security.
        # Specific error messages (like from the Gemini SDK) might leak sensitive info.
        if "API_KEY_INVALID" in str(e) or "API_KEY_SERVICE_BLOCKED" in str(e):
             return jsonify({"error": "Gemini API Error", "message": "The Gemini API key is invalid or blocked. Please check your key and try again."}), 400
        return jsonify({"error": "Gemini API Error", "message": "Failed to get response from AI. Please try again later."}), 500

def run_flask_app():
    if os.getenv("FIREBASE_EMULATORS_EXEC_MODE") == "true":
      print("Running with Firebase Emulators (exec mode) - data will persist if configured.")
    elif os.getenv("FIRESTORE_EMULATOR_HOST"):
      print(f"Running with Firestore emulator at {os.getenv('FIRESTORE_EMULATOR_HOST')}")
    
    port = int(os.environ.get('PORT', 8080))
    flask_debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=flask_debug)

if __name__ == "__main__":
    run_flask_app()
