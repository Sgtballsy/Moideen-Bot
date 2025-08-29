import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
from keep_alive import keep_alive

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GENAI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
        
    activity = discord.Activity(type=discord.ActivityType.watching, name="over Iruvazhinjippuzha")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user.name}')
    print('Moideen Ethirikkunnu...')

async def main():
    async with bot:
        await bot.load_extension('cogs.moideen_cog')
        await bot.load_extension('cogs.utility_cog')
        
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())