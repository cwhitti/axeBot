import secret as sc
from botUtilities import *
from classUtilities import *
from embedUtilities import *
from classes import name_list

class AxeBot:

    def lookup(self, msg, args, argc):

        # check for just subject lookup - ex: axe.lookup bio
        if args[1].upper() in name_list and argc == 2:

            # add subject and default term
            self.sub = args[1].upper()
            self.sms_code = self.dft_term

            # get search URL
            self.search_url = create_search_url(self)

            # begin searches
            self.url_list = get_urls(self)
            self.course_list = get_class_dict(self, "short")

            return embed_courses( self )

        # ex: CS     249
        if ( args[1].isalpha() and args[2].isdigit() ):
            # combine - CS249
            self.search_code = args[1] + args[2]
            year_pos = 4

        # ex: CS249 or 249CS or other
        else:
            self.search_code = args[1]
            year_pos = 3

        self.sub, self.cat_nbr = get_sub_nbr(self)

        # szn + year was specified - 2005
        if ( argc == year_pos + 1):

            # ensure correct szn
            self.search_szn = args[ year_pos - 1 ]
            self.search_year = args[ year_pos ]

        # Year was not specified
        else:
            self.search_szn = self.dft_szn
            self.search_year = self.dft_year

        self.sms_code = get_sms_code(self)

        self.search_url = create_search_url(self)

        # begin searches
        self.url_list = get_urls(self)
        self.course_list = get_class_dict(self, "long")

        return embed_courses( self )

    def random(self, msg, args, argc):
        return 0

    def help(self, msg, args, argc):
        return create_help_embed( self )

    def invite(self, msg, args, argc):
        return 0

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
        self.client_id = "1137314880697937940"
        self.permissions = "117824"
        self.scope = "bot"
        self.dft_szn = "fall"
        self.dft_year = "2024"
        self.dft_term = "1247"

        # custom search bitss
        self.command = "" # ex: axe.lookup
        self.search_code = "" # ex: CS249
        self.search_szn = "" # ex: "spring"
        self.search_year = "" # ex: "2018"
        self.search_url = "" # ex: HTML SEARCH URL
        self.sms_code = "" # ex: 1237
        self.sub = "" # ex: "CS"
        self.cat_nbr = "" # #ex: "249"
        self.ending = "" # ex: "WH"

        # begin HTML searches
        self.url_list = None # List of URLS on page
        self.course_list = None # Dict of all classes

        # Command dict
        self.cmd_dict = {
                        self.prefix + "lookup": (
                                                self.lookup,
                                                "Look up a specific class"
                                                ),
                        self.prefix + "random":(
                                                self.random,
                                                "Generate a random class"
                                                ),
                        self.prefix + "help":(
                                                self.help,
                                                "Use the help menu"
                                                ),
                        self.prefix + "invite":(
                                                self.invite,
                                                "Invite the bots"
                                                ),
                        }
        # end signifiers
        self.end_sigs = ['H','h','L','l','W','w','R','r','c','C']

        # season dict
        self.szn_dict = {
                        "spring":"1",
                        "summer":"4",
                        "fall":"7",
                        "winter":"8"
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
