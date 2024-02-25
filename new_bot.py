import discord
from axeBot import AxeBot
#from classes.course import Course

def run_discord_bot():

    # initialize variables
    axeBot = AxeBot()

    # set up bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client( intents=intents )

    prefix = axeBot.prefix

    #Show bot logged on successfully
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    # handle message
    @client.event
    async def on_message(msg):

        # initialize variables
        args = msg.content.split()
        argc = len(args)

        # Don't listen to self
        if msg.author == client.user or msg.attachments:
            return 0 # fail out

        # grab message contents
        if msg.content.startswith( prefix ):

            # Get command - axe.lookup
            command = args[0].lower()

            # check if command is in it
            if command in axeBot.cmd_dict.keys():

                selected_option = axeBot.cmd_dict.get( command )

                if selected_option:

                    embeds = axeBot.cmd_dict[command][0](msg, args, argc)

                    for embed in embeds:
                        await msg.channel.send(embed=embed)

                return 0

    client.run( axeBot.token )
