import re
import secret as sc
import config as cfg
from classes.NAUHandler import NAUHandler
from classes.EmbedHandler import EmbedHandler 
# from classes.GuildHandler import GuildHandler
from classes.DatabaseHandler import DatabaseHandler


class Bot( EmbedHandler, DatabaseHandler ):

    '''
    CUSTOM CLASSES 
    '''
    class SearchInfo():

        def __init__(self, msg, season, year, term, subject, nbr, ending) -> None:

            self.msg = msg
            self.season = season.capitalize()
            self.year = year
            self.term = term
            self.subject = subject
            self.nbr = nbr
            self.ending = ending

            self.search_code = f"{subject} {nbr}{ending}"
        
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
            
        def construct_url( self, course_id ):
        
            url = f"https://catalog.nau.edu/Courses/"

            return url + f"course?courseId={course_id}&term={self.term}"

            

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

                embed = await self.get_embed("unauthorized-user", 
                                            guild=msg.guild)

                return embed # return early

            # run the selected option
            embed = await selected_option[0]( msg )

        # Command not in the command dictionary
        else:  
            embed = await self.get_embed("invalid-command", 
                                            guild=msg.guild,
                                            prefix = self.prefix)

        return embed

    async def hello(self, msg):

        embed = await self.get_embed("hello",
                                guild=msg.guild,
                                prefix = self.prefix)

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

        return await self.get_embed("help", 
                                    guild = msg.guild, 
                                    desc = desc)
    
    '''
    INTEGRAL AXEBOT COMMANDS
    '''

    async def find( self, msg ):

        # initialize variables 

        # Get parameters:

            # Subject
            # Number

        # Search the database for every instance

        # Create embed

        # return embed

        return None


    async def grades( self, msg ):

        # Get parameters:
        searchInfo = self._parse_msg(msg)

        # check if we need to modify term
        if searchInfo.term == "":
            searchInfo.term = self.get_highest_term()
            searchInfo.season, searchInfo.year = self.calculate_year_and_season( searchInfo.term )

        # Set Parameters 
                # initialize variables 
        course_filters = { "search_code":searchInfo.search_code, 
                            "term":searchInfo.term
        }  
    
        # Find course in database
        courses = self.find_courses( course_filters ) 

        # if there is a course:
        if len( courses ) == 1:
            
            # Get course id
            id = courses[0].id

            section_filters = {"id":id,
                                "term":searchInfo.term
            }   

            # Create embed - 
            sections = self.find_sections( section_filters )
                                    
            print(sections)

        # if there is not a course
        else:
            
            # Recommend newest semester 
            pass

        # return embed
        return None

    async def lookup( self, msg):

        # initialize variables 

        # Get parameters:

            # Subject
            # Number
            # Term

    
        return None
        

    
    async def update_database(self, msg=None):

        # initialize variables
            # None


        # if msg != None:
        #     embed = await self.get_embed("update-database-begin",
        #                          guild=msg.guild,
        #                          end_term=self.end_term)
        #     await embed.send( msg.guild, msg.channel)

        # # try to update the db
        # try: 
        #     self.web_update()
        #     self.ready = True
            
        # # Error in updating database
        # except Exception as e:
            
        #     # Bot is not ready :(
        #     self.ready = False

        #     raise e

        # get the summary
        return None

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
        EmbedHandler.__init__( self )
        DatabaseHandler.__init__( self, 
                                 cfg.db_path, 
                                 dbg=False,
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
                            self.prefix + "grades":( self.grades,
                                                    "Find the grades for a class",
                                                    False
                            ),
                            self.prefix + "lookup":(
                                                    self.lookup,
                                                    "Look up a class",
                                                    False
                            ),
                            self.prefix + "update":(
                                                self.update_database,
                                                "Force-updates the database.",
                                                True
                            ),
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
        szn    = ""
        year   = ""
        sub    = "" # ex: "CS"
        nbr    = "" # #ex: "249"
        ending = "" # ex: "w"   
        term   = "" # ex "1247"

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

            if szn != "" and year != "":
                term = self.calculate_set_term( szn, year )

        return self.SearchInfo(msg, szn, year, term, sub, nbr, ending)