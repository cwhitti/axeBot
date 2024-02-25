import secret as sc
from botUtilities import *
from classUtilities import *

class AxeBot:

    def lookup(self, msg, args, argc):

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
        self.class_dict = get_class_dict(self)

        print(self.class_dict)

    def random(self, msg, args, argc):
        return 0

    def help(self, msg, args, argc):
        return 0

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
        self.pfx = sc.PREFIX
        self.color1 = 0x4287f5
        self.owner_id = 343857226982883339
        self.client_id = "1137314880697937940"
        self.permissions = "117824"
        self.scope = "bot"
        self.dft_szn = "fall"
        self.dft_year = "2024"

        # custom bits
        self.command = None # ex: axe.lookup
        self.search_code = None # ex: CS249
        self.search_szn = None # ex: "spring"
        self.search_year = None # ex: "2018"
        self.search_url = None # ex: HTML SEARCH URL
        self.sms_code = None # ex: 1237
        self.sub = None # ex: "CS"
        self.cat_nbr = None # #ex: "249"

        # begin HTML searches
        self.url_list = None # List of URLS on page
        self.class_dict = None # Dict of all classes

        # Command dict
        self.cmd_dict = {
                        self.pfx + "lookup":self.lookup,
                        self.pfx + "random":self.random,
                        self.pfx + "help":self.help,
                        self.pfx + "invite":self.get_invite
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
