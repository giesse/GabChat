// Import functions from the Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithRedirect, getRedirectResult, signOut, onAuthStateChanged, signInWithPopup } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

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
const googleSignInPopupButton = document.getElementById('google-signin-popup-button');
const logoutButton = document.getElementById('logout-button');
const apiKeyInput = document.getElementById('api-key-input');
const saveApiKeyButton = document.getElementById('save-api-key-button');
const deleteApiKeyButton = document.getElementById('delete-api-key-button');
const apiKeyStatusDiv = document.getElementById('api-key-status');

// Chat UI Elements
const chatHistoryDiv = document.getElementById('chat-history');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Function to append a message to the chat history
function appendMessageToChat(text, sender) {
    const messageElement = document.createElement('p');
    messageElement.textContent = text;
    messageElement.classList.add('chat-message', sender === 'user' ? 'user-message' : 'ai-message');
    chatHistoryDiv.appendChild(messageElement);
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight; // Scroll to the bottom
}

// Function to send a chat message
async function sendChatMessage() {
    const messageText = messageInput.value.trim();
    if (!messageText) {
        alert('Please enter a message.');
        return;
    }

    if (!auth.currentUser) {
        alert('Please log in to send messages.');
        return;
    }

    appendMessageToChat(`You: ${messageText}`, 'user');
    messageInput.value = ''; // Clear input field immediately
    sendButton.disabled = true; // Disable send button while waiting for reply

    try {
        const idToken = await auth.currentUser.getIdToken();
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + idToken
            },
            body: JSON.stringify({ message: messageText })
        });

        const data = await response.json();

        if (response.ok) {
            appendMessageToChat(`AI: ${data.reply}`, 'ai');
        } else {
            let errorMessage = 'Error sending message.';
            if (data && data.message) {
                errorMessage = data.message;
            } else if (data && data.error) {
                errorMessage = data.error;
            }
            appendMessageToChat(`Error: ${errorMessage}`, 'ai-error'); // Use a different class for AI errors
            alert(`Error: ${errorMessage}`); 
        }
    } catch (error) {
        console.error('Client-side error sending message:', error);
        appendMessageToChat('Client-side error sending message. See console.', 'ai-error');
        alert('Client-side error sending message. See console for details.');
    } finally {
        sendButton.disabled = false; // Re-enable send button
    }
}

// Event listener for the send button
if (sendButton) {
    sendButton.addEventListener('click', sendChatMessage);
}

// Event listener for Enter key in message input
if (messageInput) {
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default action (if any, like form submission)
            sendChatMessage();
        }
    });
}

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

        const data = await response.json(); 

        if (response.ok) { 
            if (data.has_key === true) {
                apiKeyStatusDiv.textContent = 'Gemini API Key is currently SET.';
                deleteApiKeyButton.style.display = 'block';
            } else { 
                apiKeyStatusDiv.textContent = 'Gemini API Key is NOT SET. Please enter and save your key.';
                deleteApiKeyButton.style.display = 'none';
            }
        } else { 
            console.error('Error fetching API key status:', data);
            apiKeyStatusDiv.textContent = 'Error fetching API key status. ' + (data.error || data.message || response.statusText);
            deleteApiKeyButton.style.display = 'none';
        }
    } catch (error) { 
        console.error('Client-side error fetching API key status:', error);
        apiKeyStatusDiv.textContent = 'Client-side error fetching API key status. See console for details.';
        deleteApiKeyButton.style.display = 'none';
    }
}

// Save API Key
if (saveApiKeyButton) {
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
                body: JSON.stringify({ api_key: apiKey })
            });

            const data = await response.json();
            if (response.ok) {
                alert('API Key saved successfully!');
                apiKeyInput.value = ''; 
                loadAndDisplayApiKeyStatus(); 
            } else {
                alert('Error saving API key: ' + (data.error || data.message || response.statusText));
                console.error('Error saving API key:', data);
            }
        } catch (error) {
            alert('Client-side error saving API key. See console for details.');
            console.error('Client-side error saving API key:', error);
        }
    });
}

// Delete API Key
if (deleteApiKeyButton) {
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
                loadAndDisplayApiKeyStatus(); 
            } else {
                alert('Error deleting API key: ' + (data?.error || data?.message || response.statusText));
                console.error('Error deleting API key:', data || response.statusText);
            }
        } catch (error) {
            alert('Client-side error deleting API key. See console for details.');
            console.error('Client-side error deleting API key:', error);
        }
    });
}


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

// Google Sign-In button listener (Redirect)
if (googleSignInButton) {
    googleSignInButton.addEventListener('click', () => {
        console.log("Google Sign-In button clicked (redirect method).");
        const provider = new GoogleAuthProvider();
        console.log("Provider created (redirect method):", provider);
        signInWithRedirect(auth, provider)
            .catch((error) => {
                console.error("Error initiating signInWithRedirect:", error);
            });
    });
}

// Google Sign-In button listener (Popup)
if (googleSignInPopupButton) {
    googleSignInPopupButton.addEventListener('click', () => {
        console.log("Google Sign-In button clicked (popup method).");
        const provider = new GoogleAuthProvider();
        console.log("Provider created (popup method):", provider);
        signInWithPopup(auth, provider)
            .then((result) => {
                // This gives you a Google Access Token. You can use it to access the Google API.
                const credential = GoogleAuthProvider.credentialFromResult(result);
                const token = credential.accessToken;
                // The signed-in user info.
                const user = result.user;
                console.log("Sign-in successful (popup method):", user);
                // The onAuthStateChanged listener will handle the UI updates.
            }).catch((error) => {
                // Handle Errors here.
                const errorCode = error.code;
                const errorMessage = error.message;
                // The email of the user's account used.
                const email = error.customData.email;
                // The AuthCredential type that was used.
                const credential = GoogleAuthProvider.credentialFromError(error);
                console.error("Error with signInWithPopup:", errorCode, errorMessage);
            });
    });
}

// Logout button listener
if (logoutButton) {
    logoutButton.addEventListener('click', () => {
        signOut(auth).then(() => {
            console.log("User signed out.");
        }).catch((error) => {
            console.error("Logout Error: ", error);
        });
    });
}

// Listen for authentication state changes
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log("onAuthStateChanged: User is signed in", user);
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('user-info').style.display = 'block';
        document.getElementById('user-name').textContent = user.displayName;
        document.getElementById('chat-container').style.display = 'block';
        document.getElementById('api-key-container').style.display = 'block';
        
        loadAndDisplayApiKeyStatus(); 

    } else {
        console.log("onAuthStateChanged: User is signed out");
        document.getElementById('auth-container').style.display = 'block';
        document.getElementById('user-info').style.display = 'none';
        document.getElementById('chat-container').style.display = 'none';
        document.getElementById('api-key-container').style.display = 'none';
        
        apiKeyInput.value = '';
        apiKeyStatusDiv.textContent = '';
        deleteApiKeyButton.style.display = 'none';
        chatHistoryDiv.innerHTML = ''; // Clear chat history on logout
    }
});

console.log("script.js loaded and event listeners potentially attached.");
