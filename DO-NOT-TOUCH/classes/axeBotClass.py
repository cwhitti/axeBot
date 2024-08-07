''' 





DO NOT EDIT






'''


from scripts.botUtilities import *
from scripts.classUtilities import *
from scripts.embedUtilities import *
from scripts.gradeLookupUtilities import *
from scripts.subjectAbrvs import name_list
from classes.searchClass import Search
from config import DEFAULT_TERM, DEFAULT_YEAR, DEFAULT_SZN
import secret as sc
import time

DEBUG_FLAG = False

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
                    print()
                    print("Class:", course.name)
                    print("Section:", course.section)
                    print("Instructor Name:", course.prof)
                    print("A:", course.A)
                    print("B:", course.B)
                    print("C:", course.C)
                    print("D:", course.D)
                    print("F:", course.F)
                    print("AU:", course.AU)
                    print("P:", course.P)
                    print("NG:", course.NG)
                    print("W:", course.W)
                    print("I:", course.I)
                    print("IP:", course.IP)
                    print("Pending:", course.pen)
                    print("Total:", course.total)

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
