import React from 'react';
import { AiChat, useAsBatchAdapter } from '@nlux/react';
import '@nlux/themes/nova.css';

const Chat = ({ user }) => {
  const adapter = useAsBatchAdapter(async (prompt) => {
    const idToken = await user.getIdToken();
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${idToken}`,
      },
      body: JSON.stringify({
        message: prompt,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch response.');
    }

    const data = await response.json();
    return data.reply;
  });

  return <AiChat adapter={adapter} />;
};

export default Chat;
