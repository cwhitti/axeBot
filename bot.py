import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
from class_lookup import *

prefix = 'nau.'

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

    if msg.author == client.user:
        return 0

    if msg.content == f"{prefix}hi":
        await msg.channel.send("Listening!")
        return 0

    if msg.attachments:
        # Check if there are any attachments in the message
        for attachment in msg.attachments:
                if attachment.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    return 0

    if msg.content.startswith(f"{prefix}lookup"):

        args = msg.content.split()
        input_course_code = ""

        for i in range(1, len(args)):
            input_course_code += args[i]

        url_list = get_url_list(input_course_code)
        class_dict = get_class_dict(url_list)

        if class_dict:

            for course_id, course_data in class_dict.items():

                course_name = course_data[0]
                course_description = course_data[1]
                course_units = course_data[2]
                course_prerequisites = course_data[3]

                embed = discord.Embed(title=f"{course_name}", color=0x00ff00)
                embed.add_field(name="Course ID:", value=course_id, inline=False)
                embed.add_field(name="Course Description:", value=course_description, inline=False)
                embed.add_field(name="Course Units:", value=course_units, inline=False)
                embed.add_field(name="Course Prerequisites:", value=course_prerequisites, inline=False)

                await msg.channel.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{input_course_code}", description="Sorry, we couldn't find this course.", color=0x00ff00)
            await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{prefix}prereqs"):
        embed = discord.Embed(title=f"Course Prereqs", description="Working on that!", color=0x00ff00)

  client.run(TOKEN)
