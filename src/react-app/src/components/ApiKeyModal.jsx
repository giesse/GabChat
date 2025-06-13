import React, { useState } from 'react';
import './ApiKeyModal.css';

const ApiKeyModal = ({ user, onClose, onSave }) => {
  const [apiKey, setApiKey] = useState('');

  const handleSave = async () => {
    if (!apiKey) {
      alert('Please enter an API key.');
      return;
    }
    try {
      const idToken = await user.getIdToken();
      const response = await fetch('/api/gemini-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({ api_key: apiKey })
      });
      if (response.ok) {
        onSave();
        onClose();
      } else {
        const errorData = await response.json();
        console.error('Failed to save API key:', errorData);
        alert(`Failed to save API key: ${errorData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error saving API key:', error);
      alert('An error occurred while saving the API key.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Set Your Gemini API Key</h2>
        <p>You need to set your Gemini API key to use the chat.</p>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your Gemini API Key"
        />
        <div className="modal-actions">
          <button onClick={handleSave}>Save Key</button>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default ApiKeyModal;
