import ssl
import requests
import urllib3
from secret import PREFIX, URL as url
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
    def grades( self, embed:myEmbed, search:Search ) -> bool: 

        # init variables
        courses = []        # initialize list for courses
        tries = 0

        # begin the first lookup
        success = self._grades( search, courses)

        # begin trying to get grades
        while (tries < self.max_tries) and success != True:

            # clear course list
            courses.clear()

            # increase try count
            tries += 1

            # decrease szn and year
            search.szn, search.year, search.term = search.decrease_term()

            # descrease term

            # next lookup
            success = self._grades( search, courses )


        # check if we found something
        if success == True:

            self.embedHandler.embed_grades( embed, search, courses )

        else:

            new_szn, new_yr = search.decrease_term()

            embed.add_field(name="", value= f'''
                **Term**
                {search.szn.capitalize()} {search.year}

                **What happened?**
                This class may not exist in the system due to one of the following reasons:

                👉 **Too Few Students**: To protect student privacy, grade distributions are not available for undergraduate classes with fewer than ten students enrolled or for graduate classes with fewer than five students enrolled.

                👉 **No Records**: Public records not yet available, or class does not exist.

                👉 **Off-season**: Some classes are Spring/Fall only. Try searching for another semester.

                👉 **Nonexistant Class**: There is no class with this code

                ** Suggested Commands**
                {PREFIX}help
                {PREFIX}list {search.sub} {search.szn} { int(search.year) - 1}
                {PREFIX}grades {search.sub} {search.nbr}{search.ending} {new_szn} {new_yr}
                ''',
                inline=False)

        return success
        
    
    def __init__(self, max_tries) -> None:
        self.course = None
        self.search = None
        self.max_tries = max_tries

        self.embedHandler = myEmbed()

    def _find_classes( self, soup, classCode, courses ) -> bool:
        entries = []
        info = soup.find_all('td', string=classCode)

        if info != None:

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

                # all good
                return True
        
        # No courses found
        return False
    def _get_legacy_session( self ):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        session = requests.session()
        session.mount('https://', self.CustomHttpAdapter(ctx))
        return session
    
    def _get_soup( self, resp ):

        return BeautifulSoup(resp.content, 'html.parser')
    
    def _grades(self, search:Search, courses:list )  -> bool:

        # declare variables
        term = search.term
        classSub = search.sub
        classNbr = search.nbr
        endLetter = search.ending
        classCode = classSub + " " + classNbr + endLetter

        #print(f"Now searching: {classCode} in {search.szn} {search.year}")

        # Send GET request to get initial page
        session = self._get_legacy_session()

        # Send a POST request with form data
        response = session.post( url )

        # fail out if bad page
        if not self._resp_200( response ):
            # print("This is bad")
            return False
        
        #print("We got here 1")
        
        #print( response )
        
        #print(f"resp 1= {response}\n\n\n")
        # get the soup
        soup = self._get_soup( response )

        #print(f"Soup 1= {soup}\n\n\n")

        # trigger the subject page
        response = self._post_subject( session, soup, term )

        #print(f"resp 2 = {response}\n\n\n")


        # fail out if bad page
        if response == None:
            return False
        
        #print("We got here 2")
        
        if not self._resp_200( response ):
            return False
        
        #print("We got here 3")
        
        soup = self._get_soup( response )

        #print(soup)

        response = self._post_nbr( session, soup, term, classSub, search, courses )

        if response == None:
            return False
    


        #print( type(response) )

        # if response == True or response == False:

        #     # weird recursion thing, since post_nbr works by recursively returning _grades if
        #     # we need to decrease the term. So at some point, 'response' becomes True.
        #     # That means our grades went through successfully, so it would be redundant
        #     # to send another.
        #     # This is super gross I'm sorry
        #     return response
    

        if not self._resp_200( response ):
            return False
    
        soup = self._get_soup(response)

        return self._find_classes( soup, classCode, courses )


    def _resp_200( self, resp ) -> bool:
        return resp.status_code == 200
     
    def _post_nbr( self, session, soup, term, classSub, search:Search, course:Course):

        try:

            #print(f"Incoming soup: {soup}")

            #soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
            # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
            view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

            #print(f"event validation: {event_validation}")

        # recursively go backwards so we can find the grade

        # NO DONT DO RECURSION HERE!!!!!!
        except AttributeError:

            #print("We got here 3.1")

            

            print(f"NOTHING FOUND FOR {search.szn} {search.year}")
            # search.szn, search.year = search.decrease_term( )
            # print(f" --> NOW SEARCHING {search.szn} {search.year}")

            # search.term = search.calculate_term( search.szn, search.year )

            # # should this return the bool? probably not
            # return self._grades( search, course )

            return None

            
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

            #print(f"THIS SHOULD BE 200: {response}")

            if self._resp_200( response ):
                return response
        
        # we messed up?
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