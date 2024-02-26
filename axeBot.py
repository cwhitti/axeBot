import secret as sc
import time
from botUtilities import *
from classUtilities import *
from embedUtilities import *
from classes import name_list
from searchClass import Search

class AxeBot:

    def check_cooldown(self, msg, user_cooldowns):

        if ( msg.author.id in user_cooldowns ) and ( time.time() - user_cooldowns[msg.author.id ] < self.wait_limit ):
            return True

        user_cooldowns[msg.author.id] = time.time()
        return False

    def lookup(self, msg, args, argc):

        search = Search( self.dft_szn, self.dft_year,
                         self.dft_term, self.color )

        # check if argc > 1
        if argc > 1:

            # pick args[1]
            arg1 = args[1]

            if not correct_start( arg1.upper(), name_list):

                return bad_lookup_embed( self, msg.content )

            # axe.lookup cs249, axe.lookup BIO
            if argc == 2:

                search.search_code = args[1].upper() #BIO, CS249
                search.search_year = search.dft_year
                search.sms_code = search.dft_term #1237

                if search.search_code in name_list: # ---> axe.lookup BIO

                    # add subject and default term[[
                    search.sub = search.search_code # BIO

                    ## DEFINITELY WANT SHORT DICT!!! ###
                    search.search_url = create_search_url( search )
                    search.course_list = get_class_dict_short( search )

                    if len( search.course_list ) > 0:
                        return embed_courses( search )

                else: # CS249 --->
                    search.sub, search.cat_nbr = get_sub_nbr( search )

            else:

                year_pos = -1

                if argc == 3:
                    search.search_code = args[1] + args[2]

                if argc == 4:

                    # axe.lookup cs       249 [fall 2023]
                    #if ( args[1].isalpha() and args[2].isdigit() ):

                    #    search.search_code = args[1] + args[2] # combine - CS+249
                    #    year_pos = 3

                    #axe.lookup cs249 [fall 2023]
                    #else:
                        search.search_code = args[1]
                        year_pos = 3

                if argc > 4:
                    search.search_code = args[1] + args[2] # combine - CS+249
                    year_pos = 4

                if (argc == year_pos + 1):
                    # ensure correct szn
                    search.search_szn = args[ year_pos - 1 ]
                    search.search_year = args[ year_pos ]

                # Year was not specified
                else:
                    search.search_szn = search.dft_szn
                    search.search_year = search.dft_year

                search.sms_code = get_sms_code( search )
                search.sub, search.cat_nbr = get_sub_nbr( search )

            # do the search
            search.search_url = create_search_url( search )
            search.url_list = get_urls( search )
            search.course_list = get_class_dict( search )

            #self.search_code = search.search_code

            if len( search.course_list )  > 0:
                return embed_courses( search )

        else:
            return bad_lookup_embed( self, msg.content )

    def random(self, msg, args, argc):
        return 0

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
        self.dft_szn = "fall"
        self.dft_year = "2024"
        self.dft_term = "1247"
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
