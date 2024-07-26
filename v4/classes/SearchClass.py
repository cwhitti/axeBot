from scripts.courseUtilities import *
import config

class Search:

    '''
    PUBLIC FUNCTIONS
    '''
    def calculate_term( self, szn, year):

        try:
            szn_code = self.szn_dict[szn]

        except KeyError:

            szn = self._dft_szn
            szn_code = self.szn_dict[szn]

        # POTENTIAL ISSUE: YEAR CAN BE '222q', WHERE term = 12q7
        return "1" + year[2:] + szn_code
    
    def decrease_term( self ):

        szn = self.szn.lower()
        new_yr = self.year.lower()

        # default to fall
        if szn == "spring":

            new_yr = str( int( new_yr ) - 1)
            new_szn = "winter"

        elif szn == "fall":
            new_szn = "summer"

        elif szn == "summer":
            new_szn = "spring"

        else:
            new_szn = "fall"

        return new_szn, new_yr
    
    def reset_search( self ):
        
        # initalize search stuff
        self.szn         = self._dft_szn  # ex: "spring"
        self.year        = self._dft_year # eg: "2021"
        self.term        = self._dft_term # ex: 1237
        self.sub         = "xx"  # ex: "CS"
        self.nbr         = "111" # #ex: "249"
        self.ending      = ""  # ex: "w"   
        self.search_code = self.sub + self.nbr + self.ending # ex: CS249
        self.search_url  = ""    # ex: HTML SEARCH URL

    def __init__(self, msg):

        # record user msg
        self.msg = msg

        # initialize dicts
        # basically an enumeration of the seasons but this is how NAU does it
        self.szn_dict = {
                        "spring":"1",
                        "summer":"4",
                        "fall":"7",
                        "winter":"8"
                        }

        # initialize default settings
        self._dft_szn  = config.DFT_SZN
        self._dft_year = config.DFT_YEAR
        self._dft_term = self.calculate_term( self._dft_szn, self._dft_year )
        self.color    = config.DFT_COLOR

        # initalize search stuff
        self.szn         = self._dft_szn  # ex: "spring"
        self.year        = self._dft_year # eg: "2021"
        self.term        = self._dft_term # ex: 1237
        self.sub         = "xx"  # ex: "CS"
        self.nbr         = "111" # #ex: "249"
        self.ending      = ""  # ex: "w"   
        self.search_code = self.sub + self.nbr + self.ending # ex: CS249
        self.search_url  = ""    # ex: HTML SEARCH URL

        # initialize lists
        self.end_sigs    = ['H','h','L','l','W','w','R','r','c','C']

    # debug control
    def debug(self, DEBUG_FLAG):

        if DEBUG_FLAG:

            print( "Search values:\n",
                    "\tSearch code: " + self.search_code + "\n", # ex: CS249
                    "\tsearch_szn: "  + self.szn + "\n", # ex: "spring"
                    "\tsearch_year: " + self.year + "\n", # ex: "2018"
                    "\tsearch_url: "  + self.search_url + "\n", # ex: HTML SEARCH URL
                    "\tterm: "        + self.term + "\n", # ex: 1237
                    "\tsub: "         + self.sub + "\n", # ex: "CS"
                    "\tcat_nbr: "     + self.nbr+ "\n", # #ex: "249"
                    "\tending: "      + self.ending + "\n",
                    #"\turl_list: "    + str(self.url_list) + "\n", # List of all URLS on page
                    #"\tcourse_list: " + str(self.course_list) + "\n", # Dict of all classes
                )
