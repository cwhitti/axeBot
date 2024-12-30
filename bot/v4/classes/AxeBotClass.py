import re
import config
import discord
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
    def handle_file( self, command, embed ):

        if command.startswith( self.prefix + "grades"):

            filename = config.PIE_CHART_FILE

            with open( filename, 'rb') as f:
                file = discord.File(f, filename=filename)
            
            embed.set_image(url=f'attachment://{filename}')

            return file
        
        return None
    
    def handle_msg( self, msg, logging ):

        # initialize variables
        author_id = msg.author.id
        file = None

        # Get command - axe.lookup
        argv = msg.content.split()
        command = argv[0].lower()

        # initialize embed
        embed = self.embedHandler.initialize_embed( "", "", self.dft_color )
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
                if selected_option[0]( msg, embed, logging ):

                    file = self.handle_file( command, embed )

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

        return embed, file

    def help( self, msg, embed, logging ):

        embed.title = f"{self.bot_name} Help"
        embed.description = \
            f'''
            ============== ♡ ♡ ♡ ♡ ♡ ==============
            Thank you for using {self.bot_name}!
            
            This bot was created to search up classes and grades from the 
            comfort of Discord. The intent of this bot is to improve students
            experiences searching for and enrolling in classes. 
            This bot is an independent project from a current student.

            How do you use this bot? Take a look at the commands below!
            ============== ♡ ♡ ♡ ♡ ♡ ==============
            '''

        embed.set_thumbnail(url="https://i.pinimg.com/564x/4a/25/80/4a25805f04f4ba694d9fff4a41426799.jpg")

        for key, val in self.cmd_dict.items():
            desc = val[1]
            is_admin = val[2]

            if not is_admin:
                embed.add_field(name=f"{key}", value=desc, inline=False )

        return True

    def get_github( self, msg, embed, logging ):

        return False

    def get_invite( self, msg, embed, logging ):

        return False

    def get_logs( self, msg, embed, logging ):

        # define variables
        embed.title = "Bot Logs"
        embed.description = "Sent logs via DM."
        return True
    
    def grades( self, msg, embed, logging ):

        search = Search( msg )

        embed.title = "Uh Oh..."
        embed.description = ""
        embed.set_thumbnail( url="https://lens-storage.storage.googleapis.com/png/8939f47429ad41ac8b086c18f47bd9d7")
        
        # parse message
        if not ( self._parse_msg( msg, search ) ):

            # fail out if not correct
            embed.title = "Incorrect Syntax"
            desc = f'''The correct syntax for this command is {self.prefix}grades <XXX000> <SEASON> <YEAR>
            
            NOTE: Public records are only available for classes between 2005 and {search._dft_year}'''
            
            embed.description = desc
            embed.set_footer( text=f"Try {self.prefix}help for more information." )
            return False

        ################## Look up grades for course ##################

        if not self.gradeHandler.grades( embed, search ):
            embed.title = f"Bad Search"
            embed.set_footer( text=f"Try {self.prefix}help for more information." )
            return False

        embed.title = f"{search.sub} {search.nbr} Grade Distribution"
        embed.set_thumbnail( url="https://nau.edu/wp-content/uploads/sites/183/2020/08/26_Homecoming_Parade_20191026-13-300x300.jpeg")
        return True

    def lookup( self, msg, embed, logging ):

        search = Search( msg )

        embed.title = "Uh Oh..."
        embed.description = ""
        
        # parse message
        if not ( self._parse_msg( msg, search ) ):

            # fail out if not correct
            embed.title = "Bad Search"
            desc = f'''The correct syntax for this command is {self.prefix}lookup <XXX000> <SEASON> <YEAR>
            
            NOTE: Public records are only available for classes between 2005 and {search._dft_year}'''
            
            embed.description = desc
            embed.set_footer( text=f"Try {self.prefix}help for more information.")
            return False

        ################## Look up course ##################

        course = Course()

        if not self._lookup( search, course, embed ):

            embed.set_footer( text=f"Try {self.prefix}help for more information.")
            return False

        return True

    def subj_search( self, msg, embed, logging ):

        search = Search( msg )
        
        # parse message
        if not ( self._parse_msg( msg, search ) ):

            # fail out if not correct
            embed.title = "Bad Seaech"
            desc = f'''The correct syntax for this command is {self.prefix}list <SUBJECT> <SEASON> <YEAR>
            
            NOTE: Public records are only available for classes between 2005 and {search._dft_year}'''
            
            embed.description = desc
            embed.set_footer( text=f"Try {self.prefix}help for more information.")
            return False

        course = Course()
        if not self._subj_search( search, course, embed ):

            # fail out if not correct
            embed.title = "No Records Found"
            desc = f'''The correct syntax for this command is {self.prefix}list <SUBJECT> <SEASON> <YEAR>
            
            NOTE: Public records are only available for classes between 2005 and {search._dft_year}'''
            
            embed.description = desc
            embed.set_footer( text=f"Try {self.prefix}help for more information.")
            return False
        
        embed.title = f"Courses found for {search.sub} - {search.szn.capitalize()} {search.year}"
        return True
    
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

            if (intyear > dft_year) or (intyear < 2005 ):
                return False

        except ValueError:
            year = search.year

        # fail out early if subject not in list of subjects
        if sub not in subjectAbrvs.name_list:
            return False
        
        if szn not in search.szn_dict.keys():
            szn = search.szn

        search.szn         = szn  # ex: "spring"
        search.year        = year # eg: "2021"
        search.term        = search.calculate_term( search.szn, search.year ) # ex: 1237
        search.sub         = sub  # ex: "CS"
        search.nbr         = nbr # #ex: "249"
        search.ending      = ending.upper()  # ex: "w"   
        #search.search_code = sub.upper()+nbr+ending.upper() # ex: "CS249"

        search.debug( DBG_FLAG )

        return True

    def _subj_search( self, search, course, embed ):

         # Create link #1
            # https://catalog.nau.edu/Courses/results?subject=ENG&catNbr=305&term=1247
            # Need: subject, nbr, term
        course.url1 = course.create_search_url( type="results", subject=search.sub, term=search.term)

        # https://catalog.nau.edu/Courses/results?subject=CS&catNbr=126&term=1247
        # https://catalog.nau.edu/Courses/results?subject=CS&catNbr=126&term=1247

        # REQUEST LINK CONTENTS
        code, resp = self.webHandler.search( course.url1 )

        # check if request was valid
        if code != 200 or resp == None:
            embed.description = "Yikes, something odd happened. Contact the bot owner if you see this."
            return False
        
        # Create empty list for courses
        courses = []

        # Extract course names
        for a in resp.find_all( title='view course details'):
            courses.append( a.get_text(strip=True) )

        # courses = [a.get_text(strip=True) for a in resp.find_all('a', title='view course details')]

        self.embedHandler.embed_subject( embed, courses )

        embed.set_footer(text=f"Based on {search.szn.capitalize()} {search.year} catalogue")

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
        self.max_tries    = config.MAX_TRIES
        self.subjects     = subjectAbrvs.name_list
        
        
        # intialize objects
        self.embedHandler = myEmbed()
        self.webHandler   = WebHandler()
        self.gradeHandler = GradeHandler( self.max_tries )

        # commands
        self.cmd_dict = {
                        self.prefix + "help": (
                                                self.help,
                                                "List of commands\n",
                                                False
                                                
                                                ),
                        self.prefix + "lookup": (
                                                self.lookup,
                                                f''' Look up a specific class. Defaults to the current semester.
                                                ➡ _Example: {self.prefix}lookup CS 249_
                                                ➡ _Example: {self.prefix}lookup BIO 181L Spring 2011_
                                                ➡ _Format: {self.prefix}lookup <XXX000> <season> <year>_\n''',
                                                False
                                                ),
                        self.prefix + "grades":(
                                                self.grades,
                                                f'''See grade distribution for a class. Defaults to the most recently released grades.
                                                ➡ _Example: {self.prefix}grades eng305w_
                                                ➡ _Example: {self.prefix}grades PSY255 Spring 2011_
                                                ➡ _Format: {self.prefix}grades <XXX000> <season> <year>_\n
                                                ''',
                                                False
                                                ),
                        self.prefix + "list":(
                                                self.subj_search,
                                                f''' Look up all classes under a subject
                                                ➡ _Example: {self.prefix}list eng
                                                ➡ _Example: {self.prefix}list MAT summer 2020_
                                                ➡ _Format: {self.prefix}list <SUBJECT> <season> <year>_\n''',
                                                False
                                                ),
                        # self.prefix + "invite":(
                        #                         self.get_invite,
                        #                         "Invite axeBot to your own server",
                        #                         False
                        #                         ),
                        # self.prefix + "github":(
                        #                         self.get_github,
                        #                         "View the bot's code!",
                        #                         False
                        #                         ),
                        # self.prefix + "logs":(
                        #                         self.get_logs,
                        #                         "Recieve bot logs via DM",
                        #                         True
                        #                     )
                        }




