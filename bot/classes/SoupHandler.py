import re
from bs4 import BeautifulSoup

class SoupHandler():

    def __init__(self) -> None:
        pass

    def extract_sub_codes( self, soup ):
        """
        Extracts the subject codes from the <option> elements of the select element with id 'MainContent_SubjectList'.
        
        :param html: str, HTML string containing the page content
        :return: list of extracted codes
        """

        # Find the select element with the specific id
        select_element = soup.find('select', id='MainContent_SubjectList')
        # Extract all option values within the select element
        if select_element:
            options = select_element.find_all('option')
            codes = [option['value'] for option in options]
            return codes
        return []
    def format_class_codes( self, soup ):

        class_to_course_id = {}

        # Extract the class names and courseId values
        for dt in soup.find_all("dt", class_="result-item"):
            a_tag = dt.find("a", href=True)
            if a_tag:
                course_id = a_tag["href"].split("courseId=")[1].split("&")[0]
                class_name = a_tag.get_text(strip=True)
                class_code = class_name.split(" - ")[0]
                class_to_course_id[class_code] = course_id

        return class_to_course_id
    def get_course_id( self, soup, sub, nbr, ending ):

        # print(f"LOOKING FOR {sub} {nbr}{ending}")
        # print(soup)

        # define variables
        course_id = None
        stri = f"{sub} {nbr}{ending}" + " " # the space is important 
        #print( f"\t{sub}+{nbr}+{ending}")
        
        #print(stri)

        # Extract all <tr> elements
        links = soup.find_all('a')

        # None found
        if len (links) < 2:
            return None
    
        
        # loop through links
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

                # print(f"FOUND ID: {course_id} \n\tID LINK: {link}")
                break

        #print(course_id)
        return course_id
    

    def get_course_name(self, search_soup):
        return search_soup.find("h2").text

    def get_course_description(self, search_soup):

        course_description = search_soup.find("strong", text="Description:").find_next_sibling(text=True).strip()

        # shorten if too long
        if len(course_description) > 1024:
            cont_message = ". . ."
            end_index = 1024 - len(cont_message)
            course_description = course_description[0:end_index] + cont_message

        return course_description

    def get_course_units(self, search_soup):
        return search_soup.find("strong", text="Units:").find_next_sibling(text=True).strip()

    def get_course_designation(self, search_soup):
        try:
            course_designation = search_soup.find("strong", text="Requirement Designation:").find_next_sibling(text=True).strip()

        except Exception as e:
            course_designation = "Unspecified"

        return course_designation

    def get_course_offered(self, search_soup):

        phrase = "Sections offered:"
        semesters = "No"

        try:
            strong_tag = search_soup.find("strong", text=phrase)
            
            if strong_tag:
                # Find all the sibling <a> tags after the strong tag
                semester_links = strong_tag.find_next_siblings("a")

                # Extract the text from the found links
                semesters = [link.text.strip() for link in semester_links]

                semesters = ", ".join(semesters)
        except Exception as e:
            pass

        # Join the extracted semesters into a single string
        return semesters

    def get_course_prereqs(self, search_soup):
        prereq_search = [
        "Prerequisite:",
        "Prerequisite or Corequisite:",
        "Prerequisite or Corequisite: ",
        "Pre- or Corequisite:",
        "Corequisite:"
        ]

        for phrase in prereq_search:
            try:
                course_prerequisites = search_soup.find("strong", text=phrase).find_next_sibling(text=True).strip()

                if course_prerequisites:
                    break

            except Exception as e:
                pass
                course_prerequisites = None

        return course_prerequisites
    
    def get_soup( self, resp ):

        return BeautifulSoup(resp.content, 'html.parser')