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

        self.catalog_url = "https://catalog.nau.edu/Courses/" 
        self.grades_url =  "https://www7.nau.edu/pair/reports/ClassDistribution"

    
    def get_single_course_catalog( self, subject, term, nbr, ending):

        # https://catalog.nau.edu/Courses/results?subject=ENG&catNbr=305&term=1247
        pass

    def get_nau_catalog( self, subject, term):

        # declare variables 
            # https://catalog.nau.edu/Courses/results?subject=MAT&catNbr=&term=1254
        url = self.catalog_url + f"results?subject={subject}&catNbr=&term={term}"

        # REQUEST LINK CONTENTS
        resp = self.session.get( url )

        # return thge soup
        soup = self.get_soup( resp )

        return soup

    def get_latest_term(self, soup_type ):

        if soup_type == "Catalog":
            url = self.catalog_url
        
        elif soup_type == "Grades":
            url = self.grades_url

        response = self.session.get( url )

        soup = self.get_soup( response )

        return self.get_latest_term_from_soup( soup, soup_type )

    def get_subjects_from_grades( self, term ):

        # initalize variables
            # None

        # Send POST to original URL
        response = self.session.post( self.grades_url )
        
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
    
    def get_subjects( self, term ):
        '''
        Searches the NAU grades catalog for the semester prior
        '''
        # if soup_type == "Catalog" or "Grades":
        #     term = self.decrease_term( term )
        #     url = self.catalog_url

        # response = self.session.get( url )

        # soup = self.get_soup( response )

        subjects = self.get_subjects_from_grades( term )

        if len(subjects) == 0:
            return self.get_subjects( self.decrease_term( term ) )

        return subjects

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
        response = session.post( self.grades_url, data=payload)

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

            response = self.session.post( self.grades_url, data=payload)

            if self.resp_200( response ):
                return response
        
        return None
    
    def resp_200( self, resp ) -> bool:
        return resp.status_code == 200
