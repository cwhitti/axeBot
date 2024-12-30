import requests
from bs4 import BeautifulSoup
import scripts.courseUtilities as cu

class WebHandler:

    '''
    PUBLIC FUNCTIONS
    '''
    
    def parse_course( self, resp ):

        name    = cu.get_course_name( resp)
        desc    = cu.get_course_description( resp )
        desig   = cu.get_course_designation( resp )
        units   = cu.get_course_units( resp )
        prereqs = cu.get_course_prereqs( resp )
        offered = cu.get_course_offered( resp )
        '''
        course.web_term = "" # placeholder
        course.web_catalog_year

            course.title, course.desc, course.desig, course.units, \
              course.prereqs, course.offered = self.webHandler.parse_course( resp )
        '''
        return name, desc, desig, units, prereqs, offered

    def scrape_course_id( self, resp, sub, nbr, ending="" ):

        # define variables
        course_id = None
        stri = f"{sub} {nbr}{ending} "

        # Extract all <tr> elements
        links = resp.find_all('a')
        #str="class"

        # None found
        if len (links) < 2:
            return None
        
        # looop through links
        for link in links:

            # cast it as str
            link = str( link )
            index = link.find( stri )

            # check if we found it
            if index != -1:

                # Find the start and end indices for the courseId
                start_index = link.find('courseId=') + len('courseId=')
                end_index = link.find('&', start_index)
                course_id = link[start_index:end_index]
                break

        return course_id


    # Search a url
    def search( self, url ):

        try:
            # Fetch the web page content
            response = requests.get(url)
            
            # Check if the request was successful
            if response.status_code == 200:

                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                return 200, soup
            
            # Request didnt work
            else:
                print(f"(!) Failed to retrieve the web page. Status code: {response.status_code}")
                return None, None
            
        except requests.exceptions.RequestException as e:
            print(f"(!) An error occurred: {e}")
            return None, None



    def __init__(self) -> None:
        pass