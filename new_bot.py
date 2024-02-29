import discord
from axeBot import AxeBot
import embedUtilities as eu
#from classes.course import Course

def run_discord_bot():

    # initialize variables
    axeBot = AxeBot()

    # set up bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client( intents=intents )

    prefix = axeBot.prefix

    user_cooldowns = {}

    #Show bot logged on successfully
    @client.event
    async def on_ready():

        await client.change_presence(activity=discord.Game(name="axe.help"))
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

            if axeBot.check_cooldown( msg, user_cooldowns ):

                embed = discord.Embed(title=f"Rate Limit!",
                    description="Please wait another few seconds before using this command.",
                    color=axeBot.color)

                await msg.channel.send(embed=embed)

                return 0

            # Get command - axe.lookup
            command = args[0].lower()

            # check if command is valid
            if command in axeBot.cmd_dict.keys():

                # Grab the command
                selected_option = axeBot.cmd_dict.get( command )

                async with msg.channel.typing():

                    try:
                        # create the embed list
                        embeds = axeBot.cmd_dict[command][0](msg, args, argc)

                        for embed in embeds:

                            await msg.channel.send(embed=embed)

                    except TypeError as e:

                        embed = discord.Embed(title=f"{axeBot.search_code}",
                            description=f"Sorry, we couldn't find this class",
                            color=axeBot.color)

                        await msg.channel.send(embed=embed)

                        raise e

                    except Exception as e:

                        embed = discord.Embed(title="Uh Oh!",
                            description=f"axeBot made a mistake: {e}",
                            color=axeBot.color)

                        embed.set_footer( text=f"Don't worry! Try a new commmand!")

                        await msg.channel.send(embed=embed)

                        raise e
            else:

                embed = discord.Embed(title="Uh Oh!",
                    description="Command not recognized",
                    color=axeBot.color)

                embed.set_footer( text=f"(!) Commands can be found with {axeBot.prefix}help")

                await msg.channel.send(embed=embed)
    client.run( axeBot.token )
