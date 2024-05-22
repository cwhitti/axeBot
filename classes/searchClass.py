from scripts.botUtilities import *
from scripts.classUtilities import *

class Search:

    def __init__(self, dft_szn, dft_year, dft_term, color):

        self.dft_szn = dft_szn
        self.dft_year = dft_year
        self.dft_term = dft_term
        self.color = color
        self.search_code = "" # ex: CS249
        self.search_szn = "" # ex: "spring"
        self.search_year = "" # ex: "2018"
        self.search_url = "" # ex: HTML SEARCH URL
        self.sms_code = "" # ex: 1237
        self.sub = "" # ex: "CS"
        self.cat_nbr = "" # #ex: "249"
        self.ending = ""

        # begin HTML searches
        self.url_list = [] # List of URLS on page
        self.course_list = [] # Dict of all classes

        # end signifiers
        self.end_sigs = ['H','h','L','l','W','w','R','r','c','C']

        # season dict
        self.szn_dict = {
                        "spring":"1",
                        "summer":"4",
                        "fall":"7",
                        "winter":"8"
                        }

    def clear_search( self ):

        self.dft_szn = ""
        self.dft_year = ""
        self.dft_term = ""
        self.search_code = "" # ex: CS249
        self.search_szn = "" # ex: "spring"
        self.search_year = "" # ex: "2018"
        self.search_url = "" # ex: HTML SEARCH URL
        self.sms_code = "" # ex: 1237
        self.sub = "" # ex: "CS"
        self.cat_nbr = "" # #ex: "249"
        self.ending = ""

    def all_requests( self, TYPE):

        self.search_url = create_search_url( self )
        self.url_list = get_urls( self )

        if TYPE == "Short":
            self.course_list = get_class_dict_short( self )

        else:
            self.course_list = get_class_dict( self )
    def debug(self, DEBUG_FLAG):

        if DEBUG_FLAG:

            print( "Search values:\n",
                    "\tSearch code: " + self.search_code + "\n", # ex: CS249
                    "\tsearch_szn: " + self.search_szn+ "\n", # ex: "spring"
                    "\tsearch_year: " + self.search_year+ "\n", # ex: "2018"
                    "\tsearch_url: " + self.search_url+ "\n", # ex: HTML SEARCH URL
                    "\tsms_code: " + self.sms_code+ "\n", # ex: 1237
                    "\tsub: " + self.sub+ "\n", # ex: "CS"
                    "\tcat_nbr: " + self.cat_nbr+ "\n", # #ex: "249"
                    "\tending: " + self.ending + "\n",
                    "\turl_list: " + str(self.url_list) + "\n", # List of URLS on page
                    "\tcourse_list: " + str(self.course_list) + "\n", # Dict of all classes
                )
