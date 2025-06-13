import React from 'react';
import { useAuth } from './context/AuthContext';
import SignIn from './components/SignIn';
import SignOut from './components/SignOut';
import './App.css';

function App() {
  const { currentUser } = useAuth();

  return (
    <div className="App">
      <header className="App-header">
        <h1>GabChat</h1>
        {currentUser ? <SignOut /> : <SignIn />}
      </header>
      {currentUser && (
        <main>
          <h2>Welcome, {currentUser.displayName}</h2>
          {/* Chat and API Key components will go here */}
        </main>
      )}
    </div>
  );
}

export default App;
