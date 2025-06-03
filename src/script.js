// Import functions from the Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithRedirect, getRedirectResult, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBRS6_fValVt0ZPtcLykcfcuZe2UYOEGHo",
  authDomain: "gabchat-e1851.firebaseapp.com",
  projectId: "gabchat-e1851",
  storageBucket: "gabchat-e1851.firebasestorage.app",
  messagingSenderId: "28310426932",
  appId: "1:28310426932:web:6aeec20e5dfdf84c18c161"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
console.log("Firebase Auth initialized.");

// DOM Elements
const googleSignInButton = document.getElementById('google-signin-button');
const logoutButton = document.getElementById('logout-button');
const apiKeyInput = document.getElementById('api-key-input');
const saveApiKeyButton = document.getElementById('save-api-key-button');
const deleteApiKeyButton = document.getElementById('delete-api-key-button');
const apiKeyStatusDiv = document.getElementById('api-key-status');

// Function to fetch and display API key status
async function loadAndDisplayApiKeyStatus() {
    if (!auth.currentUser) {
        apiKeyStatusDiv.textContent = 'Please log in to manage your API key.';
        deleteApiKeyButton.style.display = 'none';
        return;
    }

    try {
        const idToken = await auth.currentUser.getIdToken();
        const response = await fetch('/api/gemini-key', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + idToken
            }
        });

        const data = await response.json(); // Try to parse JSON regardless of status for error details

        if (response.ok) { // Status 200-299
            if (data.has_key === true) {
                apiKeyStatusDiv.textContent = 'Gemini API Key is currently SET.';
                deleteApiKeyButton.style.display = 'block';
            } else { // Covers has_key: false or other cases where key is not set but response is ok
                apiKeyStatusDiv.textContent = 'Gemini API Key is NOT SET. Please enter and save your key.';
                deleteApiKeyButton.style.display = 'none';
            }
        } else { // Handle errors (non-2xx responses)
            console.error('Error fetching API key status:', data); // Log the parsed JSON error data
            apiKeyStatusDiv.textContent = 'Error fetching API key status. ' + (data.error || data.message || response.statusText);
            deleteApiKeyButton.style.display = 'none';
        }
    } catch (error) { // Catch network errors or issues with response.json() if not JSON
        console.error('Client-side error fetching API key status:', error);
        apiKeyStatusDiv.textContent = 'Client-side error fetching API key status. See console for details.';
        deleteApiKeyButton.style.display = 'none';
    }
}

// Save API Key
saveApiKeyButton.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();
    if (!apiKey) {
        alert('Please enter an API key.');
        return;
    }
    if (!auth.currentUser) {
        alert('Please log in first.');
        return;
    }

    try {
        const idToken = await auth.currentUser.getIdToken();
        const response = await fetch('/api/gemini-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + idToken
            },
            body: JSON.stringify({ api_key: apiKey }) // Corrected field name to api_key
        });

        const data = await response.json();
        if (response.ok) {
            alert('API Key saved successfully!');
            apiKeyInput.value = ''; // Clear input
            loadAndDisplayApiKeyStatus(); // Refresh status
        } else {
            alert('Error saving API key: ' + (data.error || data.message || response.statusText));
            console.error('Error saving API key:', data);
        }
    } catch (error) {
        alert('Client-side error saving API key. See console for details.');
        console.error('Client-side error saving API key:', error);
    }
});

// Delete API Key
deleteApiKeyButton.addEventListener('click', async () => {
    if (!auth.currentUser) {
        alert('Please log in first.');
        return;
    }
    if (!confirm("Are you sure you want to delete your Gemini API key?")) {
        return;
    }

    try {
        const idToken = await auth.currentUser.getIdToken();
        const response = await fetch('/api/gemini-key', {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + idToken
            }
        });
        
        let data;
        try {
            data = await response.json();
        } catch (e) {
            // If response is not JSON, data will be undefined.
        }

        if (response.ok) {
            alert('API Key deleted successfully!');
            loadAndDisplayApiKeyStatus(); // Refresh status
        } else {
            alert('Error deleting API key: ' + (data?.error || data?.message || response.statusText));
            console.error('Error deleting API key:', data || response.statusText);
        }
    } catch (error) {
        alert('Client-side error deleting API key. See console for details.');
        console.error('Client-side error deleting API key:', error);
    }
});


// Handle redirect result
getRedirectResult(auth)
    .then((result) => {
        if (result) {
            console.log("getRedirectResult successful. Result:", result);
            const user = result.user;
            console.log("User object from getRedirectResult:", user);
            if (user) {
                console.log("Attempting to get ID token for user from redirect:", user.uid);
                user.getIdToken().then((idToken) => {
                    console.log("Successfully retrieved ID token from redirect:", idToken);
                    console.log("Sending token to backend for verification (from redirect)...");
                    fetch('/verify-token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({token: idToken})
                    })
                    .then(response => {
                        console.log("Backend verify-token response received (from redirect). Status:", response.status);
                        return response.json();
                    })
                    .then(data => {
                        console.log("Token verification response data (from redirect):", data);
                        if(data.status === "success"){
                            console.log("Token verification successful on backend (from redirect).");
                            // UI update will be handled by onAuthStateChanged
                        } else {
                            console.error("Token verification failed on backend (from redirect):", data.error || data.message);
                        }
                    })
                    .catch(error => {
                        console.error("Error sending token to backend or processing response (from redirect):", error);
                    });
                }).catch(error => {
                    console.error("Error getting ID token (from redirect):", error);
                });
            } else {
                 console.log("No user object in getRedirectResult, or user is null.");
            }
        } else {
            console.log("getRedirectResult: No redirect result found (this is normal on initial page load).");
        }
    })
    .catch((error) => {
        console.error("Google Sign-In Error (getRedirectResult):", error);
        console.error("Error code (getRedirectResult):", error.code);
        console.error("Error message (getRedirectResult):", error.message);
    });

// Google Sign-In button listener
googleSignInButton.addEventListener('click', () => {
    console.log("Google Sign-In button clicked (redirect method).");
    const provider = new GoogleAuthProvider();
    console.log("Provider created (redirect method):", provider);
    signInWithRedirect(auth, provider)
        .catch((error) => {
            console.error("Error initiating signInWithRedirect:", error);
        });
});

// Logout button listener
logoutButton.addEventListener('click', () => {
    signOut(auth).then(() => {
        console.log("User signed out.");
        // UI update handled by onAuthStateChanged
    }).catch((error) => {
        console.error("Logout Error: ", error);
    });
});

// Listen for authentication state changes
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in
        console.log("onAuthStateChanged: User is signed in", user);
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('user-info').style.display = 'block';
        document.getElementById('user-name').textContent = user.displayName;
        document.getElementById('chat-container').style.display = 'block';
        document.getElementById('api-key-container').style.display = 'block';
        
        loadAndDisplayApiKeyStatus(); // Load API key status

    } else {
        // User is signed out
        console.log("onAuthStateChanged: User is signed out");
        document.getElementById('auth-container').style.display = 'block';
        document.getElementById('user-info').style.display = 'none';
        document.getElementById('chat-container').style.display = 'none';
        document.getElementById('api-key-container').style.display = 'none';
        
        // Clear API key related fields
        apiKeyInput.value = '';
        apiKeyStatusDiv.textContent = '';
        deleteApiKeyButton.style.display = 'none';
    }
});

console.log("script.js loaded and event listeners potentially attached.");
