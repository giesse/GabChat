import React, { useState, useEffect } from 'react';
import { useAuth } from './context/AuthContext';
import SignIn from './components/SignIn';
import SignOut from './components/SignOut';
import UserMenu from './components/UserMenu';
import ApiKeyModal from './components/ApiKeyModal';
import Chat from './components/Chat';
import './App.css';

function App() {
  const { currentUser } = useAuth();
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [hasApiKey, setHasApiKey] = useState(false);

  useEffect(() => {
    const checkApiKey = async () => {
      if (!currentUser) return;
      try {
        const idToken = await currentUser.getIdToken();
        const response = await fetch('/api/gemini-key', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${idToken}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setHasApiKey(data.has_key);
        if (!data.has_key) {
          setIsApiKeyModalOpen(true);
        }
      } catch (error) {
        console.error('Error checking API key:', error);
        // Optionally, handle the error in the UI
      }
    };

    if (currentUser) {
      checkApiKey();
    }
  }, [currentUser]);

  const handleApiKeySaved = () => {
    setHasApiKey(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GabChat</h1>
        {currentUser ? (
          <UserMenu
            user={currentUser}
            onEditApiKey={() => setIsApiKeyModalOpen(true)}
          />
        ) : (
          <SignIn />
        )}
      </header>
      {currentUser && (
        <main>
          {hasApiKey ? (
            <Chat user={currentUser} />
          ) : (
            <h2>Welcome, {currentUser.displayName}</h2>
          )}
        </main>
      )}
      {isApiKeyModalOpen && (
        <ApiKeyModal
          user={currentUser}
          onClose={() => setIsApiKeyModalOpen(false)}
          onSave={handleApiKeySaved}
        />
      )}
    </div>
  );
}

export default App;
