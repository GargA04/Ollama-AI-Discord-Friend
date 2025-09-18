//Inital Import
const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
require("dotenv").config();
const fs = require("fs");

//Express App
const app = express();

//Middleware stopping cors error
app.use(cors());
app.use(express.json());

//Chat API
app.post('/api/chat', async (req, res) => {
  console.log("Incoming request body:", req.body);

  // Get the conversation history from the frontend
  const { messages } = req.body;

  if (!messages) {
    return res.status(400).json({ error: 'No messages provided' });
  }

   //Role Prompt for bot
  const systemPrompt = {
    role: 'system',
    content: fs.readFileSync(process.env.SYSTEM_PROMPT_FILE, "utf-8"),
  }; 


  // Prepend the system prompt to the chat history.
  // This ensures the AI always remembers its personality.
  const messagesWithSystemPrompt = [systemPrompt, ...messages];

  try {
    //Forward request to ollama with full context 
    const ollamaResponse = await fetch('http://localhost:11434/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'dolphin-mixtral',
        messages: messagesWithSystemPrompt, 
        stream: false,
      }),
    });

    if (!ollamaResponse.ok) {
      throw new Error(`Ollama API responded with status ${ollamaResponse.status}`);
    }

    const ollamaData = await ollamaResponse.json();

    //Send the AI's response back to frontend
    res.json({
        choices: [{
            message: {
                content: ollamaData.message.content
            }
        }]
    });

  } catch (error) {
    console.error('Error contacting Ollama:', error);
    res.status(500).json({ error: 'Failed to get a response from the AI backend.' });
  }
});

//Start
const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Backend server is running on http://localhost:${PORT}`);
  console.log('Personality loaded! Ready to chat.');
});
