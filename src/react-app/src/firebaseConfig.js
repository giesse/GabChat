// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

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
export const auth = getAuth(app);
