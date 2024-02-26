import requests
from bs4 import BeautifulSoup

def create_course_url(course_link):
    return f"https://catalog.nau.edu/Courses/{course_link}"

def get_course_id( url ):

    # Split the string using '&' as delimiter
    split_parts = url.split('?')

    # Loop through the split parts to find and extract the courseId
    course_id = None
    for part in split_parts:

        if part.startswith("courseId="):

            course_id_long = part.split('=')[1]
            course_id = course_id_long.split('&')[0]

def get_course_name(search_soup):
    return search_soup.find("h2").text

def get_course_description(search_soup):
    # Find the <strong> element with the text "Description:"
    course_description = search_soup.find("strong", text="Description:").find_next_sibling(text=True).strip()

    if len(course_description) > 1024:
        cont_message = ". . ."
        end_index = 1024 - len(cont_message)
        course_description = course_description[0:end_index] + cont_message

    return course_description
    
def get_course_units(search_soup):
    return search_soup.find("strong", text="Units:").find_next_sibling(text=True).strip()

def get_course_designation(search_soup):
    try:
        course_designation = search_soup.find("strong", text="Requirement Designation:").find_next_sibling(text=True).strip()

    except Exception as e:
        pass
        course_designation = "Unspecified"

    return course_designation

def get_course_prereqs(search_soup):
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
def get_course_semesters(search_soup):

    # Find the small tag containing the term information
    small_tag = search_soup.find('small')

    # Find the <small> tag within the <h1> tag
    small_tag = search_soup.find('h1', class_='mb-4 mt-4').find('small')

    # Extract the text within the <small> tag
    text = small_tag.get_text()

    # Split the text using newline and colon as delimiters
    lines = text.split('\n')
    for line in lines:
        if "Term" in line:
            course_semesters = line.split(":")[1].strip()

    return course_semesters

def get_urls(axeBot):

    # initialize variables
    url_list = []
    search_url = axeBot.search_url

    # Parse the search page HTML
    search_soup = get_search_soup(search_url)

    try:
        # Find the <dt> element with class "result-item"
        dt_elements = search_soup.find_all("dt", class_="result-item")

        for dt_element in dt_elements:

            # Find the <a> element within the <dt> element and extract the href attribute
            course_link = dt_element.find("a")["href"]

            # Construct the full URL
            course_url = create_course_url(course_link)

            url_list.append(course_url)

    except AttributeError as e:

        raise e
        return None

    return url_list

def get_search_soup(search_url):

    # Send an HTTP GET request to the search page
    search_response = requests.get(search_url)

    # Parse the search page HTML
    search_soup = BeautifulSoup(search_response.content, "html.parser")

    return search_soup
