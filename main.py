import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env file se token load karne ke liye
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setup karein
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Bot prefix define karein
bot = commands.Bot(command_prefix="??", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
  print("Bot is ready and 24/7 active!")


@bot.command(name="join")
async def join(ctx):
  # Check karein ki user kisi voice channel me hai ya nahi
  if ctx.author.voice and ctx.author.voice.channel:
    channel = ctx.author.voice.channel

    # Agar bot pehle se kisi VC me hai, toh shift ho jayega
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


# Bot run karein
bot.run(TOKEN)
