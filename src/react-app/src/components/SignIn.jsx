import React from 'react';
import { useAuth } from '../context/AuthContext';

const SignIn = () => {
  const { signinWithGoogle } = useAuth();

  const handleSignIn = async () => {
    try {
      await signinWithGoogle();
    } catch (error) {
      console.error("Error signing in with Google", error);
    }
  };

  return (
    <button onClick={handleSignIn}>
      Sign in with Google
    </button>
  );
};

export default SignIn;
