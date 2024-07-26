class Course:

    def debug( self ):
        print( self.grades )

    def create_search_url( self, type:str, subject:str = None, 
                                    catNbr:str = None, courseId:str = None,
                                        term:str = None ):
    
        url = f"{self._url_template}{type}?"
        if subject != None:
            url = f"{url}subject={subject}&"

        if catNbr != None:
            url = f"{url}catNbr={catNbr}&"

        if courseId != None:
            url = f"{url}courseId={courseId}&"

        if term != None:
            url = f"{url}term={term}&"

        url = url[:-1]
        #print( f"(!) SEARCH URL: {url}" )

        return url

    def __init__(self) -> None:
        
        self._url_template = "https://catalog.nau.edu/Courses/"
        self._grade_template = None
        self._grade_template  = ""
        self.courseID  = None   # courseId=001737
        self.term      = None   # term=1247

        #name, desc, desig, units, prereqs, offered

        self.url1 = None
        self.url2 = None
        self.web_term = None         # Fall 2024
        self.web_catalog_year = None # 2024-2025
        self.title = None        # CS 249 - Data Structures 
        self.desc  = None        # "This class designs..."
        self.units = None        # 3
        self.prereqs = None      # "CS 105 and CS 136; Pre- or Corequisite..."
        self.offered = None      # [Links]


        # Grades items
        self.name = None
        self.prof = None
        self.section = None
        self.nbr = None

        self.grades = {
                            "total": None,
                            "A": None,
                            "B": None,
                            "C": None,
                            "D": None,
                            "F": None,
                            "AU": None,
                            "P": None,
                            "NG": None,
                            "W": None,
                            "I": None,
                            "IP": None,
                            "Pen": None
                        }
    