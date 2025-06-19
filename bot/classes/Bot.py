import re
import json
import secret as sc
import config as cfg
from datetime import datetime
import classes.scripts.embeds as format
from classes.NAUHandler import NAUHandler
from classes.ChartHandler import ChartHandler
from classes.EmbedHandler import EmbedHandler 
from classes.MockDiscord import MockDiscordMsg
from classes.GuildHandler import GuildHandler
from classes.DatabaseHandler import DatabaseHandler

class Bot( EmbedHandler, DatabaseHandler, ChartHandler ):

    '''
    CUSTOM CLASSES 
    '''
    class SearchInfo( NAUHandler ):

        def __init__(self, msg=None, season=None, year=None, 
                                subject=None, nbr=None, ending=None) -> None:
            
            # initialize NAU Handler
            NAUHandler.__init__( self )

            # initialize variables
            self.msg = msg
            self.season = season
            self.year = year
            self.subject = subject
            self.nbr = nbr
            self.ending = ending

            # ensure season is in proper format
            if self.season != None:
                self.season = self.season.lower().capitalize()
            
            # calculated terms
            self.term = None
            self.search_code = f"{subject} {nbr}{ending}"

            # set up term
            self.setup()
            self.display()
            
        def construct_url( self, course_id ):
        
            url = f"https://catalog.nau.edu/Courses/"

            return url + f"course?courseId={course_id}&term={self.term}"
        
        def display( self ):

            print(f'''
                Message: {self.msg.content}
                Search Code: {self.search_code}
                Sub: {self.subject}
                Nbr: {self.nbr}
                Ending: '{self.ending}'
                Season: {self.season}
                Year: {self.year}
                Term: { self.term }
                ''')
            
        # def validate( self ):
            
        #     assert ( self.msg != None )
            
        def setup( self ):
            
            # ensure we always have a season, year, and term
            if self.season == "" or self.year == "":
                self.term = self.calculate_current_term()
                self.season, self.year = self.calculate_year_and_season( self.term  )
            
            # season and year were provided
            else:
                self.term = self.calculate_set_term( self.season, self.year )

    '''
    PUBLIC FUNCTIONS
    '''
    async def handle_command( self, msg ):

        # initialize variables
        author_id = msg.author.id

        # Get command 
        argv = msg.content.split()
        command = argv[0].lower()

        # check if command is valid
        if command in self.commands.keys():

            # Grab the command tuple
            selected_option = self.commands.get( command ) 

            # Ensure permissions, currently owner-only
            if author_id != self.owner and selected_option[2] == True:

                embed = self.get_embed("unauthorized-user", 
                                            reply_to=msg
                                            )

                return embed # return early

            # run the selected option
            embed = await selected_option[0]( msg )

        # Command not in the command dictionary
        else:  
            embed = self.get_embed("invalid-command", 
                                            reply_to=msg,
                                            prefix = self.prefix
                                        )

        return embed

    async def hello(self, msg):

        embed = self.get_embed("hello",
                                reply_to=msg,
                                prefix = self.prefix
                                )

        return embed
    
    async def help(self, msg):

        # Help command, sorry this isnt more automatic. 
        # You'll have to write it out for now
        desc=f'''Hi, thanks for using {self.name}! 
        
        This bot was created by Claire Whittington. Try out the list of commands below:
        
        🤖💬
        
        '''

        # iterate through the commands
        for trigger, tuple in self.commands.items():
            
            # get desc
            text = tuple[1]
            admin_only = tuple[2]

            if self._is_admin( msg.author ) or not admin_only:

                desc += f"**{trigger}**: {text}\n"

        return self.get_embed("help", 
                                    reply_to=msg,
                                    desc = desc
                                    )
    '''
    INTEGRAL AXEBOT COMMANDS
    '''

    async def all_sections( self, msg, search_info=None ):

        # initialize variables
        if search_info == None:

            # parse the message
            search_info = self._parse_msg( msg )
            
            # Fail out if invalid grades search
            if search_info == None:
                return self.get_embed( "invalid-command-grades",
                                            reply_to=msg,
                                            prefix=self.prefix
                                        )
            # not expecting anything so just set the 
            search_info.term = self.retrieve_highest_term( "Section" )

            # reset the season and year
            search_info.season, search_info.year = self.calculate_year_and_season( search_info.term )

        # Search the database for every instance
        id = self.retrieve_course_id( search_info.search_code, search_info.term )

        # course id was found
        if id != None:

            # grab grade records
            records = self.retrieve_sections( id )

            # if records were found:
            if len(records) > 0:

                # embed past sections
                desc = format.embed_past_sections( searchInfo=search_info, records=records )

                # return formatted embed
                return self.get_embed("all-sections",
                                            reply_to=msg,
                                            search_code=search_info.search_code,
                                            desc=desc)
            
            # Grades have never been available for this course
            else:
                return self.get_embed( "grades-unavailable-past", 
                                        reply_to=msg,
                                        search_code=search_info.search_code
                                        )

        # if there is not a course
        else:
            return self.get_embed( "course-not-found", 
                                         reply_to=msg,
                                         search_code=search_info.search_code     
            )
        
    async def current( self, msg):

        # open session
        self.open_session()

        # Get the current year and season for grades

        # Get most recent terms from nau
        catalog_term = self.get_latest_term( "Catalog" )
        grades_term  = self.get_latest_term( "Grades" )

        # Get most recent terms from my db
        last_catalog_term = self.retrieve_highest_term( "Course" )
        last_grades_term = self.retrieve_highest_term( "Section" )

        # Get the current year and season for grades
        course_season, course_year = self.calculate_year_and_season( last_catalog_term )
        grades_season, grades_year = self.calculate_year_and_season( last_grades_term )

        return self.get_embed( "current-terms",
                                    reply_to=msg,
                                    grades_season=grades_season,
                                    grades_year=grades_year,
                                    course_season=course_season,
                                    course_year=course_year,
                                    ct=catalog_term, 
                                    gt=grades_term,
                                    lct=last_catalog_term,
                                    lgt=last_grades_term)
    
    async def grades( self, msg ):

        # initialize variables
        highest_term = self.retrieve_highest_term( "Section" )

        # parse the message
        search_info = self._parse_msg( msg )
        
        # Fail out if invalid grades search
        if search_info == None:
            return self.get_embed( 
                                    "invalid-command-grades",
                                    reply_to=msg,
                                    prefix=self.prefix
                                    )
        # trigger if search term is too low
        if int( search_info.term ) < int( self.end_term):

            return self.get_embed(
                                        "term-too-low",
                                        reply_to=msg
                                        )
        
        # trigger if search term is too high, but is the current term
        if int( search_info.term ) > int( highest_term ):

            # They are looking too far ahead, like Summer 2300
            if not self.is_current_term( search_info.term ):

                return self.get_embed(
                                            "term-too-high",
                                            reply_to=msg
                                            )

            # No term provided; just set the term down to the most recent term in db
            search_info.term = highest_term

            # reset the season and year
            search_info.season, search_info.year = self.calculate_year_and_season( highest_term )

        search_info.display()

        # grab the course id
        id = self.retrieve_course_id( search_info.search_code, search_info.term )

        # course id was found
        if id != None:

            # grab grade records
            records = self.retrieve_sections( id, search_info.term )

            # if records were found:
            if len(records) > 0:

                desc = format.embed_grades( records )

                embed = self.get_embed( "grades",
                                            reply_to=msg,
                                            search_code=search_info.search_code,
                                            desc=desc,
                                            season="SZN",
                                            year="YEAR"
                                            )
                
                # set the embed's file
                embed.set_file ( filepath=self.create_figure( search_info, records ) )
                return embed
            
            # A course ID exists for this, but no sections
            else:
                
                # find all instances of this section
                return await self.all_sections( msg, search_info=search_info )

        # if there is not a course
        else:
            return self.get_embed( "course-not-found", 
                                         reply_to=msg,
                            )
            
            # Recommend newest semester 

        # return embed
        return None

    async def lookup( self, msg):

        # initialize variables 

        # Get parameters:

            # Subject
            # Number
            # Term

    
        return None
        
    async def test_commands( self, msg ):

        # initialize variables
        commands = [ 
                    f"{self.prefix}help",

                    f"{self.prefix}all sta471",

                    f"{self.prefix}grades",
                    f"{self.prefix}grades cs 126l",
                    f"{self.prefix}grades cs126l",
                    f"{self.prefix}grades cs126l fall 2023",

                    f"{self.prefix}lookup",
                    f"{self.prefix}lookup cs 126l",
                    f"{self.prefix}lookup cs126l",
                    f"{self.prefix}lookup cs126l fall 2023",

                    # current 
                    f"{self.prefix}current",
                    ]
        passed = 0
        failed = 0
        desc = ""

        # loop though commands
        for command in commands:

            # create a msg object
            custom_msg = MockDiscordMsg( 
                                        content = command,
                                        author  = msg.author,
                                        channel = msg.channel,
                                        guild   = msg.guild
                                        )

            # attempt handling
            try:
                
                # try embed
                tested_embed = await self.handle_command( custom_msg )
                #tested_embed.reply_to = None
                #await tested_embed.send( msg.guild )

                # get success embed 
                embed = self.get_embed( 
                                        "unit-test-success",
                                        channel=msg.channel.name,
                                        context=command,
                                      )
                
                
                # add extras
                if tested_embed != None:

                    # set description
                    embed.description = tested_embed.description[0:100] + " . . ." 

                    # set file if exists
                    if tested_embed.filepath != None:
                        
                        # set the file
                        embed.set_file( filepath=tested_embed.filepath )

                passed += 1
                desc += f"✅ {command}\n"
                    
            # something went wrong, format 
            except Exception as e:
                
                print(e)
                embed = self.get_embed( 
                                        "unit-test-failure",
                                        channel=msg.channel,
                                        context=command,
                                        e=e
                                        )
                
                desc += f"❌ {command}\n"

            # send the unit test embed
            await embed.send( msg.guild )

        # send summary embed
        return self.get_embed( "unit-test-desc",
                                reply_to=msg,
                                passed=passed,
                                failed=failed,
                                desc=desc)


    '''
    PRIVATE FUNCTIONS
    '''
    def __init__(self, name, client, prefix, dft_color, TOKEN):

        # Define ready flag
        self.ready = False

        # initialize important stuff
        self.client     = client    # discord client o bject
        self.name       = name      # str
        self.dft_color  = dft_color # hex
        self.prefix     = prefix    # str
        self.token      = TOKEN     # str | TODO: make this environmental variable

        # initialize additional file variables
        self.invite_link = sc.invite_link # str
        self.admin_list = cfg.admin_list  # list of ints (discord IDs)
        self.owner      = cfg.owner       # int (discord ID)

        # validation stuff
        self.required_roles    = [ ] # list of string names for roles
        self.required_channels = [ "general" ] # list of string names for channels

        # initialize inherited classes
        NAUHandler.__init__( self )
        ChartHandler.__init__( self )
        GuildHandler.__init__( self )
        EmbedHandler.__init__( self )
        DatabaseHandler.__init__( self, 
                                 db_path  = cfg.db_path, 
                                 dbg      = cfg.dbg,
                                 reset_db = cfg.reset_db,
                                 )

        # initialize all available commands for users to call
        self.commands = {   
                            self.prefix + "hello": ( self.hello,
                                                    "Test me to say hello!",
                                                    False
                            ),
                            self.prefix + "help": ( self.help, # command to run
                                                    "List of commands", # help desc
                                                    False, # is admin-only command
                            ),
                            self.prefix + "all":(
                                                    self.all_sections,
                                                    "List all semesters that have publically viewable grades for a specified class",
                                                    False

                            ),
                            self.prefix + "grades":( self.grades,
                                                    "Find the grades for a class",
                                                    False
                            ),
                            self.prefix + "lookup":(
                                                    self.lookup,
                                                    "Look up a class",
                                                    False
                            ),
                            self.prefix + "current":(
                                                    self.current,
                                                    "List the current semester supported by this bot",
                                                    False
                            ),
                            self.prefix + "test":(
                                                    self.test_commands,
                                                    "Unit test the bot",
                                                    True
                            )
                            # self.prefix + "retrieve":(
                            #                         self.user_retrieve,
                            #                         "Send a query to the database",
                            #                         True
                            # )
                            # self.prefix + "update":(
                            #                     self.update_database,
                            #                     "Force-updates the database.",
                            #                     True
                            # ),
                        }
    def _is_admin(self, author):
        return author.id in self.admin_list
    
    def _match( self, str):
        # Use a regular expression to match the parts
        match = re.match(r"([A-Za-z]*)(\d*)([A-Za-z]*)", str)
        
        if match:
            # Filter out empty groups and put the groups into a list
            parts = [group for group in match.groups() if group]
            
            return parts
        else:
            return []
        
    def _parse_msg( self, msg ):

        # initialize variables
        argv = ( msg.content.lower() ).split()
        argc   = len( argv )
        szn    = "" # ex" "Spring"
        year   = "" # ex: "2009"
        sub    = "" # ex: "CS"
        nbr    = "" # #ex: "249"
        ending = "" # ex: "w"   

        # make sure there are enough args
        if ( ( argc < 2 or argc > 5) ):
            return None

        # case: 2 args
            # axe.lookup CS126L
        if argc == 2:
            
            # grab args
            val1 = argv[1]

            # handle CS/CS249/CS249W
            searchList = self._match( val1 )
            items = len( searchList )

            if items >= 1:
                sub = searchList[0].upper()
            
            if items >= 2:
                nbr = searchList[1]

            if items >= 3:
                ending = searchList[2]


        # case: 3 args
            # axe.lookup	CS	249w
        elif argc == 3:

            # grab args
            sub = argv[1].upper()
            val2 = argv[2]

            # handle CS/CS249/CS249W
            searchList = self._match( val2 )
            items = len( searchList )

            if items >= 1:
                nbr = searchList[0]
            
            if items >= 2:
                ending = searchList[1]


        # case: 4 args
            # axe.lookup	CS	    Fall	2022
            # axe.lookup	CS249w	Fall	2022
        elif argc == 4:

            # grab args
            val1 = argv[1]
            val2 = argv[2]
            val3 = argv[3]

            # handle CS/CS249/CS249W
            searchListVal1 = self._match( val1 )
            itemsVal1 = len( searchListVal1 )

            if itemsVal1 >= 1:
                
                sub = searchListVal1[0].upper() # CS

                if itemsVal1 >= 2:
                    nbr = searchListVal1[1] # 249

                if itemsVal1 >= 3:
                    ending = searchListVal1[2] # w

            # assign season/year
            szn = val2
            year = val3

        # case: 5 args
            # axe.lookup	CS	249w	Fall	2022
        elif argc == 5:

            # grab args
            val1 = argv[1]
            val2 = argv[2]
            val3 = argv[3]
            val4 = argv[4]

            # handle CS/CS249/CS249W
            searchListVal1 = self._match( val1 )
            itemsVal1 = len( searchListVal1 )

            if itemsVal1 >= 1:
                
                sub = searchListVal1[0].upper()

                if itemsVal1 >= 2:
                    nbr = searchListVal1[1]

                if itemsVal1 >= 3:
                    ending = searchListVal1[2]


            searchList = self._match( val2 )
            items = len( searchList )

            if items >= 1:
                nbr = searchList[0]
            
            if items >= 2:
                ending = searchList[1]

            szn = val3
            year = val4
        
        return self.SearchInfo( msg, szn, year, sub, nbr, ending.upper() )