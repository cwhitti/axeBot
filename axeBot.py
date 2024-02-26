import secret as sc
from botUtilities import *
from classUtilities import *
from embedUtilities import *
from classes import name_list
from searchClass import Search

class AxeBot:

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
                search.sms_code = search.dft_term #1237

                if search.search_code in name_list: # ---> axe.lookup BIO

                    # add subject and default term[[
                    search.sub = search.search_code # BIO

                    ## DEFINITELY WANT SHORT DICT!!! ###
                    search.search_url = create_search_url( search )
                    search.course_list = get_class_dict_short( search )

                    if len( search.course_list )  > 0:
                        return embed_courses( search )

                else: # CS249 --->
                    search.sub, search.cat_nbr = get_sub_nbr( search )

            else:

                year_pos = -1

                if argc == 3:
                    search.search_code = args[1] + args[2]

                if argc == 4:

                    # axe.lookup cs       249 [fall 2023]
                    if ( args[1].isalpha() and args[2].isdigit() ):

                        search.search_code = args[1] + args[2] # combine - CS+249
                        year_pos = 4

                    #axe.lookup cs249 [fall 2023]
                    else:
                        search.search_code = args[1]
                        year_pos = 3

                if argc > 4:
                    search.search_code = args[1] + args[2] # combine - CS+249

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

            if len( search.course_list )  > 0:
                return embed_courses( search )

        else:
            return bad_lookup_embed( self, msg.content )

    def random(self, msg, args, argc):
        return 0

    def help(self, msg, args, argc):
        return [create_help_embed( self )]

    def invite(self, msg, args, argc):
        return 0

    def github(self, msg, args, argc):

        return github_embed( self )

    def get_invite(self, msg, args, argc):

        # build url
        addr = "https://discord.com/api/oauth2/authorize?"
        client_id = f"client_id={self.client_id}"
        perms = f"&permissions={self.permissions}"
        scope = f"&scope={self.scope}"

        # return url
        return addr + client_id + perms + scope

    def __init__(self):
        # variables
        self.token = sc.TOKEN
        self.prefix = sc.PREFIX
        self.color = 0x4287f5
        self.owner_id = 343857226982883339
        self.gitLink = "https://github.com/cwhitti/axeBot"
        self.client_id = "1137314880697937940"
        self.permissions = "117824"
        self.scope = "bot"
        self.dft_szn = "fall"
        self.dft_year = "2024"
        self.dft_term = "1247"

        # Command dict
        self.cmd_dict = {
                        self.prefix + "lookup": (
                                                self.lookup,
                                                "Look up a specific class"
                                                ),
                        #self.prefix + "random":(
                        #                        self.random,
                        #                        "Generate a random class"
                        #                        ),
                        self.prefix + "help":(
                                                self.help,
                                                "Use the help menu"
                                                ),
                        #self.prefix + "invite":(
                        #                        self.invite,
                        #                        "Invite the bots"
                        #                        ),
                        self.prefix + "github":(
                                                self.github,
                                                "View the bot's code!"
                                                ),
                        }


    def clear_search(self):
        # custom bits
        self.command = "" # ex: axe.lookup
        self.search_code = "" # ex: CS249
        self.search_szn = "" # ex: "spring"
        self.search_year = "" # ex: "2018"
        self.search_url = "" # ex: HTML SEARCH URL
        self.sms_code = "" # ex: 1237
        self.sub = "" # ex: "CS"
        self.cat_nbr = "" # # ex: "249"
        self.ending = "" # ex: "WH"

        # clear lists
        self.clear_url_list()
        self.clear_course_list()

    def clear_url_list(self):

        self.url_list.clear()

    def clear_course_list(self):

        self.course_list.clear()
