import discord
from discord.ext import commands
import re
import unicodedata
import os
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

base_variants = [
    "nigger", "nigga", "n1gger", "n1gga", "ni99er", "ni99a",
    "n!gger", "n!gga", "n¡gga", "n¡gger", "n|gga", "n|gger"
]

def normalize_message(msg):
    msg = msg.lower()
    msg = unicodedata.normalize('NFKD', msg)
    msg = ''.join(c for c in msg if c.isalnum())
    return msg

blocked_patterns = [
    re.compile(rf"{variant.replace('n', '[nñ]').replace('g', '[g69q]')}", re.IGNORECASE)
    for variant in base_variants
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    normalized = normalize_message(message.content)

    for pattern in blocked_patterns:
        if pattern.search(normalized):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, that word is not allowed here.",
                delete_after=5
            )
            return

    await bot.process_commands(message)

# Web server to keep Railway app alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

# Run the bot using the token from environment variables
bot.run(os.environ["MTM2OTQ4OTc3MTQxNTYwMTIyMw.GzLSdY.GzQfQ0TXRs_Fun6ycemQKUjj6t7mKPCrYweF2w"])
