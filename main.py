import os
import threading
import discord
from discord.ext import commands
from flask import Flask

# 1. Flask App setup (Render ke liye taaki 24/7 online rahe)
app = Flask('')


@app.route('/')
def home():
  return "Bot is alive and running 24/7!"


def run_flask():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = threading.Thread(target=run_flask)
  t.start()


# 2. Discord Bot setup
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="??", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
  print("Bot is ready and 24/7 active!")


@bot.command(name="join")
async def join(ctx):
  if ctx.author.voice and ctx.author.voice.channel:
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
      await ctx.voice_client.move_to(channel)
    else:
      await channel.connect()
    await ctx.send(f"Connected to **{channel.name}**!")
  else:
    await ctx.send("Pehle aap kisi Voice Channel me join toh karo!")


@bot.command(name="leave")
async def leave(ctx):
  if ctx.voice_client:
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected from the voice channel.")
  else:
    await ctx.send("Bot kisi voice channel me nahi hai!")


# 3. Flask web server start karo aur phir bot run karo
if __name__ == "__main__":
  keep_alive()
  bot.run(TOKEN)
