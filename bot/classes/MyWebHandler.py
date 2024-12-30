from secret import url
from classes.NAUHandler import NAUHandler
from classes.SoupHandler import SoupHandler
from classes.LegacyHttpHandler import LegacyHttpHandler

class MyWebHandler( LegacyHttpHandler, NAUHandler, SoupHandler ):


    def __init__(self) -> None:
        
        LegacyHttpHandler.__init__( self )
        SoupHandler.__init__( self )
        NAUHandler.__init__( self )
        self.session = None
        self.saved_soup = None

    def retrieve_id(self, subject, nbr, term, ending):

        response = self.get_nau_catalog( subject, nbr, term, ending )

        soup = self.get_soup(response)

        return self.get_course_id(soup, subject, nbr, ending)
    
    def get_nau_catalog( self, subject, nbr, term, ending):

        # declare variables 

        # Create link #1
            # https://catalog.nau.edu/Courses/results?subject=ENG&catNbr=305&term=1247
            # Need: subject, nbr, term
        url = f"https://catalog.nau.edu/Courses/results?subject={subject}&catNbr={nbr}{ending}&term={term}"

        # REQUEST LINK CONTENTS
        resp = self.session.get( url )

        print(url)

        return resp

        # # check if request was valid
        # if code != 200 or resp == None:
        #     embed.description = "Yikes, something odd happened. Contact the bot owner if you see this."
        #     return False
        
        # # pull its course ID
        # course.courseID = self.webHandler.scrape_course_id( resp, search.sub, 
        #                                                             search.nbr, 
        #                                                                 search.ending )
        
        # # Course was not found
        # if course.courseID == None:
        #     embed.description = "This class does not exist."
        #     return False

    def get_subjects( self, term ):

        # initalize variables
            # None

        # Send POST to original URL
        response = self.session.post( url )
        
        # fail out if bad page
        if not self.resp_200( response ):
            return [] # returns empty list
        
        # get the soup
        soup = self.get_soup( response )

        # trigger the subject page
        response = self.post_term( self.session, soup, term )

        # fail out if bad page
        if not self.resp_200( response ):
            return [] # returns empty list

        # get the soup
        soup = self.get_soup( response )

        # save the soup for later use
        self.save_soup = soup

        # return the extracted codes
        return self.extract_sub_codes( soup )
    
    def open_session( self ):
        self.session = self.get_legacy_session()
    
    def post_term( self, session, soup, term ):
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

        self.saved_soup = self.get_soup( response )

        if not self.resp_200( response ):
            return None
    
        return response

    def post_subject( self, term, subject ):

        # initialize vairables
        resp = None

        # get the saved soup
        soup = self.saved_soup

        # Open session
        if self.session == None:
            self.session = self.open_session()

        # try finding the viewstate and event validation
        try:

            #print(f"Incoming soup: {soup}")

            view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

        # Fall out if not found
        except AttributeError:
            return resp

        # Ensure it exists
        if (event_validation != None):

            # Prepare the payload with updated form data and the extracted values
            payload = {
                "__VIEWSTATE": view_state,
                "__EVENTVALIDATION": event_validation,
                "ctl00$MainContent$TermList": term,         # Fall 2023
                "ctl00$MainContent$SubjectList": subject,   # CS
                "ctl00$MainContent$Button1": "Submit"
            }

            response = self.session.post(url, data=payload)

            if self.resp_200( response ):
                return response
        
        return None
    
    def resp_200( self, resp ) -> bool:
        return resp.status_code == 200
