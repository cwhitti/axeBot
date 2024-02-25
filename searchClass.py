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
