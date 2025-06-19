import os
import json
import discord
import datetime
import config as cfg
from discord.utils import get
from classes.GuildHandler import GuildHandler

# Overarching handler
class EmbedHandler ( ):

    # Custom embed class
    class CustomEmbed( discord.Embed ):

        def __init__(self, *, channel_name, **kwargs):
            super().__init__(**kwargs)
            self.channel_name = channel_name
            self.channel_obj = None
            self.guild = None
            self.file_obj = None
            self.filepath = None
            self.reply_to = None

        def set_file(self, *, filepath: str=None):
            """
            Embeds an image into the embed from the given file path.

            Parameters:
            - filepath (str): The path to the image file.

            Returns:
            - discord.File: The file object to be sent with the embed.
            """

            file = discord.File(filepath, filename=filepath.split("/")[-1])
            self.set_image(url=f"attachment://{file.filename}")
            
            self.file_obj = file
            self.filepath = filepath


        def set_guild(self, guild):
            self.guild = guild

        def set_channel_obj( self ):
            self.channel_obj = get(self.guild.channels, name=self.channel_name)


        async def send( self, guild ):
            """Sends the embed to the assigned channel."""

            # Set embed parameters
            self.set_guild( guild )
            self.set_channel_obj( )

            # send the embed
            if self.channel_obj is not None:

                # Send the embed
                async with self.channel_obj.typing():
                    
                    # See if we need to reply to someone
                    if self.reply_to != None:

                        # reply to the message with file
                        if self.file_obj != None:
                            await self.reply_to.reply(embed=self, file=self.file_obj)
                        
                        # reply to the message WITHOUT file
                        else:
                            await self.reply_to.reply(embed=self)
                    
                    #else, simply send the message
                    else:                        
                        # send embed with file
                        if self.file_obj != None:
                            await self.channel_obj.send(embed=self, file=self.file_obj)
                        
                        # send embed WITHOUT file
                        else:
                            await self.channel_obj.send(embed=self)

            else:
                raise ValueError(f"Embed '{self.title}' needs a channel in order to be sent!.")

    # init
    def __init__(self ):

        self._json_file = cfg.json_file

        self._color_map = {
            "DEFAULT":cfg.dft_color,
            "SUCCESS":cfg.success_color,
            "FAILURE":cfg.error_color
        }

        self.guild = None

        with open(self._json_file, 'r') as embed_file:
            self.messages = json.load(embed_file)

    def get_embed(self, key, reply_to = None, **kwargs):

        # get embed format
        data = self._get_embed_format( key )

        # set channel
        if "channel" in kwargs.keys():
            channel_name = kwargs["channel"]

        # set reply_to
        elif reply_to != None:
            channel_name = reply_to.channel.name

        else:
            # retrieve channel name 
            channel_name = data.get("channel")

        # handle setting channel name if not supplied
        if channel_name == "":
            if reply_to is not None:
                channel_name = reply_to.channel.name

            if channel_name == "":
                raise ValueError("ERROR: get_embed must specify which channel embed needs to be sent to.")

        # create embed with channel obj
        embed = EmbedHandler.CustomEmbed(
            title=data.get("title").format(**kwargs),             # format the title w args
            description=data.get("description").format(**kwargs), # format the body w args
            color=self._color_map[(data.get("color"))],           # Get the hex color
            channel_name = channel_name,                          # set destination channel
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc), # set timestamp    
        )

        # set reply_to
        if reply_to != None:
            embed.reply_to = reply_to

        # set footer
        embed.set_footer(text=data.get("footer").format(**kwargs))

        # return the embed
        return embed
    
    def _get_embed_format( self, key ):

        data = self.messages.get(key)

        if not data:
            raise ValueError(f"Embed key '{key}' not found in configuration.")
        
        return data

