#Inital Imports
import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get env vars
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#Get Url for backend communication
BACKEND_URL = "http://localhost:3002/api/chat"

#Discord intents standard
intents = discord.Intents.default()
intents.message_content = True

#Prefix so communication with bot can happen
prefix = "Ai-chan "
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Store per-user conversation history
user_histories = {}

#User interaction
@bot.event
async def on_message(message):
    #Stops self answering
    if message.author == bot.user:
        return

    #Check the event starts with real prefix
    if message.content.startswith(prefix):
        #Get User message as well as who sent it
        user_message = message.content[len(prefix):]
        user_id = str(message.author.id)

        # Initialize history if new user
        if user_id not in user_histories:
            user_histories[user_id] = []

        # Save user’s message
        user_histories[user_id].append({"role": "user", "content": user_message})

        #Make payload with user context 
        payload = {"messages": user_histories[user_id]}

        #Send Message to backend and send back response to user
        try:
            #Sends Channel typing indicator
            async with message.channel.typing():
                async with aiohttp.ClientSession() as session:
                    #Wait for response from backend with the payload
                    async with session.post(BACKEND_URL, json=payload, timeout=240) as resp:
                        data = await resp.json()
                        ai_reply = data["choices"][0]["message"]["content"]
                        await message.channel.send(ai_reply)

                        # Save bot’s reply
                        user_histories[user_id].append({"role": "assistant", "content": ai_reply})
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
