import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
from class_lookup import *

prefix = 'nau!'

def run_discord_bot():
  TOKEN = 'MTEzNzMxNDg4MDY5NzkzNzk0MA.GXxLQq.7xCp2p_8tAIhbU-WyRgP5hs2k73dK49KM_Ukvc'
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  #Show bot logged on successfully
  @client.event
  async def on_ready():
    print(f'{client.user} is now running!')

  @client.event
  async def on_message(msg):

    if msg.content.startswith(f"{prefix}class"):

        main()



  client.run(TOKEN)
