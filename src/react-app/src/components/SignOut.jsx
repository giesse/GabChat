import React from 'react';
import { useAuth } from '../context/AuthContext';

const SignOut = () => {
  const { signout } = useAuth();

  const handleSignOut = async () => {
    try {
      await signout();
    } catch (error) {
      console.error("Error signing out", error);
    }
  };

  return (
    <button onClick={handleSignOut}>
      Sign Out
    </button>
  );
};

export default SignOut;
