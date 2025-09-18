# Discord Chat Bot using Ollama

This is a **Discord chatbot** powered by [Ollama](https://ollama.ai/) running the **Dolphin Mixtral** model.
The bot responds to messages in your server using a custom role/system prompt that you can define.

---

## Requirements 

* [Python 3.9+](https://www.python.org/downloads/)
* [Discord Developer Account](https://discord.com/developers/applications)
* [Ollama](https://ollama.ai/download) installed and running locally
* **Dolphin Mixtral model** pulled into Ollama

  ```bash
  ollama pull dolphin-mixtral
  ```

---

## Setup 

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** → give it a name.
3. Navigate to **Bot** → **Add Bot**.
4. Copy the **Bot Token** (you’ll need this later).
5. Under **Privileged Gateway Intents**, enable:

   * Message Content Intent
   * Server Members Intent
     
6. When Adding to a server make sure to add **Read Message History** and **Send Messages** are also ticked off

### 2. Clone this Repository

```bash
git clone https://github.com/GargA04/Ollama-AI-Discord-Friend.git
cd Ollama-AI-Discord-Friend
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a System Prompt

The bot uses a **role prompt** to define its personality and behavior.
You must create a file named exactly:

```
system_prompt.txt
```

Place it in the **root directory** of the project (same level as `launcher.py`).

Example contents:

```text
You are a helpful AI chatbot that answers like a Discord friend.
```

### 5. Add Your Bot Token

Create a `.env` file in the root directory:

```
DISCORD_TOKEN=your-discord-bot-token-here
```

---

## Running the Bot 

Start the bot with:

```bash
python launcher.py
```

The bot will connect to Discord and start responding to messages in servers where it has permission.

---

## Notes 
* Ensure the **system\_prompt.txt** file exists and is spelled exactly like that.
* If you want to change the bot’s behavior, just edit `system_prompt.txt` and restart the bot.





