import discord
from discord.ext import commands
import subprocess
import os
import sys
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from class_lookup import *
import math
from classes import name_list

class axeBot:
    def __init__(self, token = None, prefix = None, color = None):
        self.token = token
        self.prefix = prefix
        self.color = color
        self.wait_limit = 5

def run_discord_bot(axeBot = axeBot):
  load_dotenv()  # Load environment variables from .env file
  axeBot = initialize_bot(axeBot)
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  user_cooldowns = {}

  #Show bot logged on successfully
  @client.event
  async def on_ready():
    print(f'{client.user} is now running!')

  @client.event
  async def on_message(msg):

    if msg.author == client.user: # Ensure bot doesnt listen to self
        return 0

    if msg.content == f"{axeBot.prefix}hi": # Testrun
        await msg.channel.send("Listening! :D!")
        return 0

    if (msg.author.id == 343857226982883339) and (msg.content == f"{axeBot.prefix}end"):
        print(f"{client.user} is now stopped.")
        await client.close()

    if (msg.author.id == 343857226982883339) and (msg.content == f"{axeBot.prefix}update"):
        result = update_bot()
        embed = discord.Embed(title=f"", description=result, color=axeBot.color)
        await msg.channel.send(embed=embed)
        print("restarting...")
        restart_bot()

    if (msg.author.id == 343857226982883339) and (msg.content == f"{axeBot.prefix}restart"):
        await(msg.channel.send("Restarting..."))
        print("restarting")
        restart_bot()

    if msg.content == f"{axeBot.prefix}invite":
        print("https://discord.com/api/oauth2/authorize?client_id=1137314880697937940&permissions=274877966336&scope=bot")

    if msg.attachments: # Check if there are any attachments in the message
        for attachment in msg.attachments:
                if attachment.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    return 0

    if msg.content.startswith(f"{axeBot.prefix}random"): # Gen random class
        async with msg.channel.typing():
            # Check if the user is on cooldown
            if msg.author.id in user_cooldowns and time.time() - user_cooldowns[msg.author.id] < axeBot.wait_limit:  # 5 seconds cooldown
                embed = discord.Embed(title=f"Rate Limit!", description="Please wait another few seconds before using this command.", color=axeBot.color)
                await msg.channel.send(embed=embed)

                return 0
            else:
                # Update the user's last message time
                user_cooldowns[msg.author.id] = time.time()

            class_dict = random_class()
            course_id_list = list(class_dict.keys())
            course_id = course_id_list[0]

            embed = one_embed_course(axeBot, course_id, class_dict[course_id])
            await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{axeBot.prefix}help"):
        async with msg.channel.typing():
            embed = create_help_embed(axeBot)
            await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{axeBot.prefix}subjects"):
        async with msg.channel.typing():
            embed = create_subjects_embed(axeBot, name_list)
            await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{axeBot.prefix}lookup"):
        async with msg.channel.typing():

            # Check if the user is on cooldown
            if msg.author.id in user_cooldowns and time.time() - user_cooldowns[msg.author.id] < axeBot.wait_limit:  # 5 seconds cooldown
                embed = discord.Embed(title=f"Rate Limit!", description="Please wait another few seconds before using this command.", color=axeBot.color)
                await msg.channel.send(embed=embed)

                return 0
            else:
                # Update the user's last message time
                user_cooldowns[msg.author.id] = time.time()

            args = msg.content.split()
            input_course_code = ""

            if len(args) == 1:
                embed = discord.Embed(title=f"Sorry, didn't catch that!", description=f"You can look up a class by using {axeBot.prefix}lookup <XXX000>", color=axeBot.color)
                await msg.channel.send(embed=embed)
                return 0

            for i in range(1, len(args)):
                input_course_code += args[i]

            subject, cat_nbr = get_sub_nbr(input_course_code)
            url_list = get_urls(subject, cat_nbr)

            # Embed the full class
            if len(url_list) <= 5:
                class_dict = get_class_dict(url_list)

                if class_dict:
                    for course_id, course_data in class_dict.items():
                        #embed course
                        embed = one_embed_course(axeBot, course_id, course_data)
                        await msg.channel.send(embed=embed)

                else:
                    embed = discord.Embed(title=f"{input_course_code}", description="Sorry, we couldn't find this course.", color=axeBot.color)
                    await msg.channel.send(embed=embed)

            # shows a list of names to look up
            elif len(url_list) > 5:
                # just grab the name and class ID
                class_dict = get_class_dict_short(subject, cat_nbr)

                if class_dict:
                    items_per_embed = 25 # discord embed limit
                    total_items = len(class_dict)
                    course_ids = list(class_dict.keys())

                    first_embed = True

                    for i in range(0, total_items, items_per_embed):
                        batch_keys = course_ids[i:i + items_per_embed]
                        embed = batch_embed_course(axeBot, batch_keys, class_dict, first_embed)
                        await msg.channel.send(embed=embed)
                        first_embed = False
                else:
                    embed = discord.Embed(title=f"{input_course_code}", description="Sorry, we couldn't find this course.", color=axeBot.color)
                    await msg.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"{input_course_code}", description="Sorry, we couldn't find this course.", color=axeBot.color)
                await msg.channel.send(embed=embed)

    if msg.content.startswith(f"{axeBot.prefix}prereqs"):
        embed = discord.Embed(title=f"Course Prereqs", description="Working on that!", color=axeBot.color)
        await msg.channel.send(embed=embed)

  client.run(axeBot.token)

def initialize_bot(axeBot):
    axeBot = axeBot()
    axeBot.token = os.getenv('DISCORD_TOKEN')
    axeBot.prefix = os.getenv('PREFIX')
    axeBot.color = 0xAAFF00

    return axeBot

def create_help_embed(axeBot):

    embed = discord.Embed(title="Axe Bot Help", description="List of available commands:", color=axeBot.color)
    embed.add_field(name=f"{axeBot.prefix}help", value="Show a list of commands", inline=False)
    embed.add_field(name=f"{axeBot.prefix}sujects", value="Look up all class subjects at NAU", inline=False)
    embed.add_field(name=f"{axeBot.prefix}lookup <XXX>", value="Look up all classes for a specific subject", inline=False)
    embed.add_field(name=f"{axeBot.prefix}lookup <XXX000>", value="Look up a specific class", inline=False)
    embed.add_field(name=f"{axeBot.prefix}random", value="Find a random class", inline=False)
    embed.add_field(name=f"{axeBot.prefix}prereqs", value="Show course prerequisites (work in progress)", inline=False)
    embed.set_footer(text="(!) This bot is not affiliated, sponsored, nor endorsed by NAU.")

    return embed

def create_subjects_embed(axeBot,name_list):

    embed = discord.Embed(title="NAU Subjects", description="List of available topics:", color=axeBot.color)

    start_letter = 'A'
    name_string = ""

    for name in name_list:

        if name_string != "":

            if name[0] == start_letter:
                name_string += f", {name}"

            else:
                embed.add_field(name="", value=name_string, inline=False)
                start_letter = name[0]
                name_string = ""
        else:
            name_string = f"{name}"

    embed.add_field(name="", value=name_string, inline=False)

    return embed

def one_embed_course(axeBot,course_id, course_data):

    course_name = course_data[0]
    course_description = course_data[1]
    course_units = course_data[2]
    course_prerequisites = course_data[3]
    course_designation = course_data[4]
    course_semesters = course_data[5]
    course_url = create_course_url(f"course?courseId={course_id}&term=1237")

    embed = discord.Embed(title=course_name, description="", color=axeBot.color)
    embed.add_field(name="Course ID:", value=course_id, inline=False)
    embed.add_field(name="Course Description:", value=course_description, inline=False)
    embed.add_field(name="Course Units:", value=course_units, inline=False)
    embed.add_field(name="Course Semesters:", value=course_semesters, inline=False)
    embed.add_field(name="Course Designation:", value=course_designation, inline=False)
    embed.add_field(name="Course Prerequisites:", value=course_prerequisites, inline=False)
    embed.add_field(name="", value=f"[Course Link]({course_url})", inline=False)

    return embed

def batch_embed_course(axeBot,batch_keys, class_dict, first_embed):

    if first_embed == True:
        embed = discord.Embed(title=f"{len(class_dict)} RESULTS FOUND", color=axeBot.color)

    else:
        embed = discord.Embed(title="", color=axeBot.color)

    for course_id in batch_keys:
        course_name = class_dict[course_id]
        embed.add_field(name=course_name, value=f"CourseID: {course_id}", inline=False)
    return embed

def update_bot():

    try:
        subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT, cwd='/root/bots/axeBot')
        result = f"Bot updated successfully!"

    except subprocess.CalledProcessError as e:
        error_message = e.output.decode('utf-8')
        result = f"Bot update failed: {error_message}"

    return result

def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)
