import discord
from discord.ext import commands
import os
import time
import requests
from bs4 import BeautifulSoup
from class_lookup import *

prefix = 'nau.'

# Create a dictionary to store user cooldowns
user_cooldowns = {}

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
        # Check if the user is on cooldown
        if msg.author.id in user_cooldowns and time.time() - user_cooldowns[msg.author.id] < 5:  # 5 seconds cooldown
            embed = discord.Embed(title=f"Rate Limit!", description="Please wait another few seconds before using this command.", color=0x00ff00)
            await msg.channel.send(embed=embed)

            return 0
        else:
            # Update the user's last message time
            user_cooldowns[msg.author.id] = time.time()

        args = msg.content.split()
        input_course_code = ""

        if len(args) == 1:
            embed = discord.Embed(title=f"Sorry, didn't catch that!", description=f"You can look up a class within NAU by using {prefix}lookup <XXX000>", color=0x00ff00)
            await msg.channel.send(embed=embed)
            return 0

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
                course_designation = course_data[4]

                embed = discord.Embed(title=f"{course_name}", color=0x00ff00)
                embed.add_field(name="Course ID:", value=course_id, inline=False)
                embed.add_field(name="Course Description:", value=course_description, inline=False)
                embed.add_field(name="Course Units:", value=course_units, inline=False)
                embed.add_field(name="Course Designation:", value=course_designation, inline=False)
                embed.add_field(name="Course Prerequisites:", value=course_prerequisites, inline=False)

                await msg.channel.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{input_course_code}", description="Sorry, we couldn't find this course.", color=0x00ff00)
            await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{prefix}prereqs"):
        embed = discord.Embed(title=f"Course Prereqs", description="Working on that!", color=0x00ff00)

  client.run(TOKEN)
