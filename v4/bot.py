import discord
import logging
from secret import LOG_FILE
from classes.AxeBotClass import AxeBot

def run_discord_bot( ):

    # Configure logging
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                        format='%(asctime)s %(levelname)s %(message)s')

    # Discord requirements
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client( intents=intents )

    # initialize variables
    axeBot = AxeBot( client )
    prefix = axeBot.prefix

    #Show bot logged on successfully
    @client.event
    async def on_ready():

        await client.change_presence(activity=discord.Game(name=f"{prefix}help"))
        print(f'Starting {client.user}')

    # handle message
    @client.event
    async def on_message(msg):

        # Don't listen to self
        if msg.author == client.user or msg.attachments:
            return 0 # dont respond

        # grab message contents
        if msg.content.startswith( prefix ):

            embed, file = axeBot.handle_msg(msg, logging)

            async with msg.channel.typing():

                if file != None:
                     await msg.reply( embed=embed, file=file )

                else:

                    await msg.reply( embed=embed )

                return 0

    client.run( axeBot._TOKEN )