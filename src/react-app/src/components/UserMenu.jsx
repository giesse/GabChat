import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import SignOut from './SignOut';
import './UserMenu.css';

const UserMenu = ({ user, onEditApiKey }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { signOut } = useAuth();

  const handleSignOut = () => {
    signOut();
    setIsOpen(false);
  };

  const handleEditApiKey = () => {
    onEditApiKey();
    setIsOpen(false);
  };

  return (
    <div className="user-menu">
      <button onClick={() => setIsOpen(!isOpen)} className="user-menu-button">
        {user.displayName || 'User'}
      </button>
      {isOpen && (
        <div className="user-menu-dropdown">
          <ul>
            <li onClick={handleEditApiKey}>Edit API Key</li>
            <li onClick={handleSignOut}>Sign Out</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
