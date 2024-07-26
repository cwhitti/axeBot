import re
import config
import secret as sc
from datetime import datetime
from classes.SearchClass import Search
from classes.CourseClass import Course
from classes.EmbedClass import myEmbed
import scripts.subjectAbrvs as subjectAbrvs
from classes.WebHandlerClass import WebHandler
from classes.GradeHandlerClass import GradeHandler

DBG_FLAG = False 

class AxeBot:
    '''
    PUBLIC FUNCTIONS
    '''

    def handle_msg( self, msg, logging ):

        # initialize variables
        author_id = msg.author.id

        # Get command - axe.lookup
        argv = msg.content.split()
        command = argv[0].lower()

        # initialize embed
        embed = self.embedHandler.initialize_embed( "Title", "Desc", self.dft_color )
        embed.timestamp = datetime.now()
        # embed.set_footer( text='\u200b',icon_url=self.client.user.avatar.url )

        # check if command is valid
        if command in self.cmd_dict.keys():

            # Grab the command tuple
            selected_option = self.cmd_dict.get( command ) 

            # Ensure permissions, currently owner-only
            if author_id != self.owner and selected_option[2] == True:

                # set stuff
                embed.title = "Unauthorized Command"
                embed.description = "Sorry, only authorized users can use this command."

                return embed # return early
            
            # Permissions are fine, try executing
            try:
                # create the embed list
                selected_option[0]( msg, embed, logging )

            # Catch TypeError
            except TypeError as e:

                embed.title = "TypeError"
                embed.description = f"{e}"
                embed.color = config.ERR_COLOR
                embed.set_footer( text=f"Don't worry! Try a new commmand!")
                raise e

            # Catch others
            except Exception as e:

                print("(!) Something went wrong.")
                raise e

        # Command not in the command dictionary
        else:  
            embed.title = "Invalid Command"
            embed.description = "Command not recognized."
            embed.set_footer( text=f"(!) Commands can be found with {self.prefix}help")

        return embed

    def help( self, msg, embed, logging ) -> None:

        embed.title = f"{self.bot_name} Help"
        embed.description = \
            f'''Thanks for using {self.bot_name}. 
            <HELP DESC>
            
            ============== ♡ ♡ ♡ ♡ ♡ =============='
            
            This bot was created to search up classes from the comfort
            of Discord. Because looking for classes can be annoying,
            the creators of this bot wanted a novel way to search them up.

            Usage examples:
            **Lookup**
            - {self.prefix}lookup CS249
            - {self.prefix}lookup BIO 181L Spring 2011 
            - {self.prefix}lookup cs212 summer 2017  
            **Grades**
            - {self.prefix}grades CS126L 
            - {self.prefix}grades mat136 summer 2022  
            **Subjects**
            - {self.prefix}subjects  
            **Invite**
            - {self.prefix}invite    
            
            (!) This bot is not affiliated, sponsored, nor endorsed by NAU (!)
            "**+===+ All Commands +===+**"'''

        for key, val in self.cmd_dict.items():
            desc = val[1]
            is_admin = val[2]

            if not is_admin:
                embed.add_field(name=key, value=desc, inline=True )

    def get_github( self, msg, embed, logging ):
        pass 

    def get_invite( self, msg, embed, logging ):
        pass

    def get_logs( self, msg, embed, logging ) -> None:

        # define variables
        embed.title = "Bot Logs"
        embed.description = "Sent logs via DM."

    def grades( self, msg, embed, logging ):

        search = Search( msg )

        embed.title = "Uh Oh..."
        embed.description = "Default"
        
        # parse message
        if not ( self._parse_msg( msg, search ) ):

            # fail out if not correct
            embed.title = "Bad Search"
            embed.description = f"The correct syntax for this command is {self.prefix}grades <XXX000> <SEASON> <YEAR>"
            embed.set_footer( text=f"Try {self.prefix}help for more information." )
            return False

        ################## Look up grades for course ##################

        if not self.gradeHandler.grades( embed, search ):
            embed.set_footer( text=f"Try {self.prefix}help for more information." )


    def lookup( self, msg, embed, logging ):

        search = Search( msg )

        embed.title = "Uh Oh..."
        embed.description = "Default"
        
        # parse message
        if not ( self._parse_msg( msg, search ) ):

            # fail out if not correct
            embed.title = "Bad Search"
            embed.description = f"The correct syntax for this command is {self.prefix}lookup <XXX000> <SEASON> <YEAR>"
            embed.set_footer( text=f"Try {self.prefix}help for more information.")
            return False

        ################## Look up course ##################

        course = Course()

        if not self._lookup( search, course, embed ):

            embed.set_footer( text=f"Try {self.prefix}help for more information.")

    def subjects( self, msg, embed, logging ):
        pass
    
    '''
    PRIVATE FUNCTIONS
    '''
    def _lookup( self, search:Search, course:Course, embed:myEmbed ):

        # declare variables 

        # Create link #1
            # https://catalog.nau.edu/Courses/results?subject=ENG&catNbr=305&term=1247
            # Need: subject, nbr, term
        course.url1 = course.create_search_url( type="results", subject=search.sub, catNbr=search.nbr, term=search.term)

        # https://catalog.nau.edu/Courses/results?subject=CS&catNbr=126&term=1247
        # https://catalog.nau.edu/Courses/results?subject=CS&catNbr=126&term=1247

        # REQUEST LINK CONTENTS
        code, resp = self.webHandler.search( course.url1 )

        # check if request was valid
        if code != 200 or resp == None:
            embed.description = "Yikes, something odd happened. Contact the bot owner if you see this."
            return False
        
        # pull its course ID
        course.courseID = self.webHandler.scrape_course_id( resp, search.sub, 
                                                                    search.nbr, 
                                                                        search.ending )
        
        # Course was not found
        if course.courseID == None:
            embed.description = "This class does not exist."
            return False
            
        # Create link #2
            # https://catalog.nau.edu/Courses/course?courseId=010050&term=1247
            # Need: courseId, term
        course.url2 = course.create_search_url( type="course", courseId=course.courseID, term=search.term )

        code, resp = self.webHandler.search( course.url2 )

        # check if request was valid
        if code != 200 or resp == None:
            embed.description = "Yikes, something odd happened. Contact the bot owner if you see this."
            return False

        # Assign everything
        course.title, course.desc, course.desig, course.units, \
            course.prereqs, course.offered = self.webHandler.parse_course( resp )
        
        # Finish up the embed
        self.embedHandler.embed_course( embed, course, search )

        # woohoo!
        return True
    
    def _parse_msg( self, msg, search:Search ):

        # initialize variables
        argv = ( msg.content.lower() ).split()
        argc   = len( argv )
        sub    = "" # ex: "CS"
        nbr    = "" # #ex: "249"
        ending = "" # ex: "w"   
        szn    = search.szn
        year   = search.year

        # make sure there are enough args
        if ( ( argc < 2 or argc > 5) ):
            return False

        # case: 2 args
            # axe.lookup CS249w
        if argc == 2:
            
            # grab args
            val1 = argv[1]

            # handle CS/CS249/CS249W
            searchList = self._match_( val1 )
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
            searchList = self._match_( val2 )
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
            searchListVal1 = self._match_( val1 )
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
            searchListVal1 = self._match_( val1 )
            itemsVal1 = len( searchListVal1 )

            if itemsVal1 >= 1:
                
                sub = searchListVal1[0].upper()

                if itemsVal1 >= 2:
                    nbr = searchListVal1[1]

                if itemsVal1 >= 3:
                    ending = searchListVal1[2]


            searchList = self._match_( val2 )
            items = len( searchList )

            if items >= 1:
                nbr = searchList[0]
            
            if items >= 2:
                ending = searchList[1]

            szn = val3
            year = val4

        # validate year and szn
        try: 
            intyear = int( year )
            dft_year = int( search._dft_year )

            if (intyear > dft_year):
                return False

        except ValueError:
            year = search.year

        # fail out early if subject not in list of subjects
        if sub not in subjectAbrvs.name_list:
            return False

        search.szn         = szn  # ex: "spring"
        search.year        = year # eg: "2021"
        search.term        = search.calculate_term( search.szn, search.year ) # ex: 1237
        search.sub         = sub  # ex: "CS"
        search.nbr         = nbr # #ex: "249"
        search.ending      = ending.upper()  # ex: "w"   

        search.debug( DBG_FLAG )

        return True

    '''
    PROTECTED FUNCTIONS
    '''

    def _match_( self, str):
        # Use a regular expression to match the parts
        match = re.match(r"([A-Za-z]*)(\d*)([A-Za-z]*)", str)
        
        if match:
            # Filter out empty groups and put the groups into a list
            parts = [group for group in match.groups() if group]
            
            return parts
        else:
            return []
        
    def __init__(self, client):

        # init client
        self.client         = client

        # # init filenmes
        # self.whitelist_file = config.WHITELISTFILE
        # self.bot_file       = config.BOTFILE

        # # grab lists
        # self.whitelist    = self.get_whitelist()
        # self.bot_dict     = self.get_bot_dict()
        # self.msp_servers  = self.bot_dict.keys()
        
        # variables
        self.bot_name     = sc.BOT_NAME
        self._TOKEN       = sc.TOKEN
        self.prefix       = sc.PREFIX
        self.owner        = config.OWNER
        self.dft_color    = config.DFT_COLOR
        self.log_file     = config.LOG_FILE
        self.subjects     = subjectAbrvs.name_list

        # initialize tables
        
        # intialize objects
        self.embedHandler = myEmbed()
        self.webHandler   = WebHandler()
        self.gradeHandler = GradeHandler()

        # commands
        self.cmd_dict = {
                        self.prefix + "help": (
                                                self.help,
                                                "List of commands",
                                                False
                                                
                                                ),
                        self.prefix + "lookup": (
                                                self.lookup,
                                                f"Look up a specific class\nFormat: {self.prefix}lookup <XXX000> <season> <year>",
                                                False
                                                ),
                        self.prefix + "grades":(
                                                self.grades,
                                                "See grade distribution for a class",
                                                False
                                                ),
                        self.prefix + "subjects":(
                                                self.subjects,
                                                "See all course subjects",
                                                False
                                                ),
                        self.prefix + "invite":(
                                                self.get_invite,
                                                "Invite axeBot to your own server",
                                                False
                                                ),
                        self.prefix + "github":(
                                                self.get_github,
                                                "View the bot's code!",
                                                False
                                                ),
                        self.prefix + "logs":(
                                                self.get_logs,
                                                "Recieve bot logs via DM",
                                                True
                                            )
                        }




'''

class AxeBot:

    async def send_file_and_get_url(self, channel, file_path):

        # Send the file asynchronously and get the message object
        message = await channel.send(file=discord.File(file_path))

        # Return the URL of the uploaded file
        return message.attachments[0].url

    def check_cooldown(self, msg, user_cooldowns):

        if ( msg.author.id in user_cooldowns ) and ( time.time() - user_cooldowns[msg.author.id ] < self.wait_limit ):
            return True

        user_cooldowns[msg.author.id] = time.time()
        return False

    def parse_search(self, msg, args, argc, search):

        search.search_szn = search.dft_szn
        search.search_year = search.dft_year

        # check if argc > 1
        if argc > 1:

            TYPE = "LONG"

            # pick args[1]
            arg1 = args[1]

            if not correct_start( arg1.upper(), name_list):
                return False

            # axe.lookup cs249, axe.lookup BIO
            if argc == 2:

                search.search_code = args[1].upper() #BIO, CS249
                search.search_year = search.dft_year
                search.sms_code = search.dft_term #1237

                if search.search_code in name_list: # ---> axe.lookup BIO

                    TYPE = "SHORT"

                    # add subject and default term[[
                    search.sub = search.search_code # BIO

                    ## DEFINITELY WANT SHORT DICT!!! ###
                    #search.search_url = create_search_url( search )
                    #search.course_list = get_class_dict_short( search )

                else: # CS249 --->
                    search.sub, search.cat_nbr = get_sub_nbr( search )

            # axe.lookup cs249 Fall, axe.lookup BIO181 Fall 2022
            else:

                year_pos = -1

                if argc == 3:
                    search.search_code = args[1] + args[2]

                if argc == 4:
                    search.search_code = args[1]
                    year_pos = 3

                if argc > 4:
                    search.search_code = args[1] + args[2] # combine - CS+249
                    year_pos = 4

                if (argc == year_pos + 1):

                    search.search_szn = args[ year_pos - 1 ]
                    search.search_year = args[ year_pos ]

                search.sms_code = get_sms_code( search )
                search.sub, search.cat_nbr = get_sub_nbr( search )

            search.all_requests( TYPE )

        if len( search.course_list ) > 0 :
            return True

        return False

    def lookup(self, msg, args, argc):

        search = Search( self.dft_szn, self.dft_year,
                         self.dft_term, self.color )

        if self.parse_search( msg, args, argc, search):
            return embed_courses( search )

        return bad_lookup_embed( self, msg.content )

    def grades(self, msg, args, argc):

        search = Search( self.dft_szn, self.dft_year,
                         self.dft_term, self.color )

        embeds = []

        if self.parse_search( msg, args, argc, search):

            courses = get_grades( search )

            if len(courses) == 0:
                return class_not_offered( search )

            for course in courses:

                if DEBUG_FLAG:


                embeds.append(create_grade_embed( search, course ))

            return embeds

        return bad_grade_lookup( self, search )

    def help(self, msg, args, argc):
        return [create_help_embed( self )]

    def github(self, msg, args, argc):

        return github_embed( self )

    def subjects(self, msg, args, argc):

        return [ create_subjects_embed( self, name_list ) ]

    def get_invite(self, msg, args, argc):

        # build url
        addr = "https://discord.com/api/oauth2/authorize?"
        client_id = f"client_id={self.client_id}"
        perms = f"&permissions={self.permissions}"
        scope = f"&scope={self.scope}"

        url = addr + client_id + perms + scope

        # return url
        return [invite_embed( self, url )]

    def __init__(self):
        # variables
        self.token = sc.TOKEN
        self.prefix = sc.PREFIX
        self.color = 0x4287f5
        self.owner_id = 343857226982883339
        self.wait_limit = 5
        self.gitLink = "https://github.com/cwhitti/axeBot"
        self.client_id = "1137314880697937940"
        self.permissions = "117824"
        self.scope = "bot"
        self.dft_szn = DEFAULT_SZN
        self.dft_year = DEFAULT_YEAR
        self.dft_term = DEFAULT_TERM
        self.search_code = ""

        # Command dict
        self.cmd_dict = {
                        self.prefix + "help": (
                                                self.help,
                                                "List of commands"
                                                ),
                        self.prefix + "lookup": (
                                                self.lookup,
                                                f"Look up a specific class\nFormat: {self.prefix}lookup <XXX000> <season> <year>"
                                                ),
                        self.prefix + "grades":(
                                                self.grades,
                                                "See grade distribution for a class"
                                                ),
                        self.prefix + "subjects":(
                                                self.subjects,
                                                "See all course subjects"
                                                ),
                        #self.prefix + "random":(
                        #                        self.random,
                        #                        "Generate a random class"
                        #                        ),
                        self.prefix + "invite":(
                                                self.get_invite,
                                                "Invite axeBot to your own server"
                                                ),
                        self.prefix + "github":(
                                                self.github,
                                                "View the bot's code!"
                                                ),
                        }
                        
'''