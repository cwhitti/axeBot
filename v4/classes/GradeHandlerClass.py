import ssl
import requests
import urllib3
from secret import URL as url
from bs4 import BeautifulSoup
from classes.CourseClass import Course
from classes.SearchClass import Search
from classes.EmbedClass import myEmbed



class GradeHandler:

    class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

        def __init__(self, ssl_context=None, **kwargs):
            self.ssl_context = ssl_context
            super().__init__(**kwargs)

        def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = urllib3.poolmanager.PoolManager(
                num_pools=connections, maxsize=maxsize,
                block=block, ssl_context=self.ssl_context)

    '''
    PUBLIC FUNCTIONS
    '''    
    def grades( self, embed:myEmbed, search:Search ):

        # initialize list for courses
        courses = []

        if not self._grades( search, courses ):
            embed.description = "Sorry, we were unable to find the grades for this course."
            return False

        self.embedHandler.embed_grades( embed, search, courses )
        return True
        
    
    def __init__(self) -> None:
        self.course = None
        self.search = None

        self.embedHandler = myEmbed()

    def _get_legacy_session( self ):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        session = requests.session()
        session.mount('https://', self.CustomHttpAdapter(ctx))
        return session
    
    def _get_soup( self, resp ):
        return BeautifulSoup(resp.content, 'html.parser')
    
    def _grades(self, search:Search, courses:list ):

        # declare variables
        term = search.term
        classSub = search.sub
        classNbr = search.nbr
        endLetter = search.ending
        classCode = classSub + " " + classNbr + endLetter

        # Send GET request to get initial page
        session = self._get_legacy_session()

        # Send a POST request with form data
        response = session.post( url )

        # fail out if bad page
        if not self._resp_200( response ):
            return False
        
        # get the soup
        soup = self._get_soup( response )

        # trigger the subject page
        response = self._post_subject( session, soup, term )

        # fail out if bad page
        if response == None:
            return False
        
        soup = self._get_soup(response)

        response = self._post_nbr( session, soup, term, classSub, search, courses )

        if response == None:
            return False

        soup = self._get_soup(response)

        entries = []
        info = soup.find_all('td', string=classCode)

        for td_tag in info:

            tr_tag = td_tag.parent  # Get the parent <tr> tag
            entry = [td.text for td in tr_tag.find_all('td')]
            entries.append(entry)

        if len(entries) != 0:

            for entry in entries:

                course = Course()

                course.name = entry[0]
                course.section = entry[1]
                course.nbr = entry[2]
                course.prof = entry[3]
                
                a = entry[4]
                b = entry[5]
                c = entry[6]
                d = entry[7]
                f = entry[8]
                au = entry[9]
                p = entry[10]
                ng = entry[11]
                w = entry[12]
                i = entry[13]
                ip = entry[14]
                pen = entry[15]
                total = entry[16]

                course.grades = {
                                    "total": total,
                                    "A": a,
                                    "B": b,
                                    "C": c,
                                    "D": d,
                                    "F": f,
                                    "AU": au,
                                    "P": p,
                                    "NG": ng,
                                    "W": w,
                                    "I": i,
                                    "IP": ip,
                                    "Pen": pen
                                }

                courses.append( course )

        return True

    def _resp_200( self, resp ):
        return resp.status_code == 200
     
    def _post_nbr( self, session, soup, term, classSub, search:Search, course:Course):

        try:
            # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
            view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

        # recursively go backwards so we can find the grade
        except AttributeError:

            search.szn, search.year = search.decrease_term( )

            search.term = search.calculate_term( search.szn, search.year )

            self._grades( search, course )

        if (event_validation != None):

            # Prepare the payload with updated form data and the extracted values
            payload = {
                "__VIEWSTATE": view_state,
                "__EVENTVALIDATION": event_validation,
                "ctl00$MainContent$TermList": term,  # Fall 2023
                "ctl00$MainContent$SubjectList": classSub,
                "ctl00$MainContent$Button1": "Submit"
            }

            response = session.post(url, data=payload)

            if self._resp_200( response ):
                return response
            
        print(" Something went wrong again")
        return None
    
    def _post_subject( self, session, soup, term ):
            # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

        # Prepare the payload with updated form data and the extracted values
        payload = {
            "__VIEWSTATE": view_state,
            "__EVENTVALIDATION": event_validation,
            "ctl00$MainContent$TermList": term,  # Fall 2023
        }

        # send the payload
        response = session.post(url, data=payload)

        if not self._resp_200( response ):
            return None
        
        return response