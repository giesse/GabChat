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
                            console.error("Token verification failed on backend (from redirect):", data.error);
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

// Google Sign-In button
const googleSignInButton = document.getElementById('google-signin-button');
googleSignInButton.addEventListener('click', () => {
    console.log("Google Sign-In button clicked (redirect method).");
    const provider = new GoogleAuthProvider();
    console.log("Provider created (redirect method):", provider);
    signInWithRedirect(auth, provider)
        .catch((error) => {
            // This catch is for errors during the initiation of the redirect
            console.error("Error initiating signInWithRedirect:", error);
        });
    // Note: signInWithRedirect itself doesn't return a promise that resolves with user credentials here.
    // The result is handled by getRedirectResult after the redirect.
});

// Logout
const logoutButton = document.getElementById('logout-button');
logoutButton.addEventListener('click', () => {
    signOut(auth).then(() => {
        console.log("User signed out.");
        // Update UI handled by onAuthStateChanged
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
    } else {
        // User is signed out
        console.log("onAuthStateChanged: User is signed out");
        document.getElementById('auth-container').style.display = 'block';
        document.getElementById('user-info').style.display = 'none';
        document.getElementById('chat-container').style.display = 'none';
        document.getElementById('api-key-container').style.display = 'none';
    }
});

// Placeholder for API key saving and chat message sending
// JavaScript for sign-in, chat, and API key management will go here