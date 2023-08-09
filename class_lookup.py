import requests
from bs4 import BeautifulSoup
from classes import name_list
import random

def get_sub_nbr(input_course_code):

    lower_course_code = input_course_code.replace(" ","")

    end_signifiers = ['H','h','L','l','W','w','R','r']

    course_code = lower_course_code.upper()

    if course_code not in name_list:
        if course_code[-1] in end_signifiers:
            if course_code[-2] in end_signifiers: # Has an ending like "ENV301WH"
                if len(course_code) == 7:
                    subject = course_code[:3]
                    cat_nbr = course_code[3:]

                elif len(course_code) == 8:
                    subject = course_code[:3]
                    cat_nbr = course_code[3:]

                else:
                    subject = 'aaa'
                    cat_nbr = '000'
            else: # Has an ending like "ENV301W"
                if len(course_code) == 6:
                    subject = course_code[:2]
                    cat_nbr = course_code[2:]

                elif len(course_code) == 7:
                    subject = course_code[:3]
                    cat_nbr = course_code[3:]

                elif len(course_code) == 8:
                    subject = course_code[:4]
                    cat_nbr = course_code[4:]

                else:
                    subject = 'aaa'
                    cat_nbr = '000'
        else: # Has no ending, like "BIO181"
            if len(course_code) == 5:
                subject = course_code[:2]
                cat_nbr = course_code[2:]

            elif len(course_code) == 6:
                subject = course_code[:3]
                cat_nbr = course_code[3:]

            elif len(course_code) == 7:
                subject = course_code[:4]
                cat_nbr = course_code[4:]
            else:
                subject = 'aaa'
                cat_nbr = '000'
    else: # Subject is in name list
        subject = course_code
        cat_nbr = ""

    return subject, cat_nbr

def get_urls(subject, cat_nbr): #returns a list of URLS for a lookup

    url_list = []

    # URL of the search page
    search_url = f"https://catalog.nau.edu/Courses/results?subject={subject}&catNbr={cat_nbr}&term=1237"

    # Send an HTTP GET request to the search page
    search_response = requests.get(search_url)

    # Parse the search page HTML
    search_soup = BeautifulSoup(search_response.content, "html.parser")

    try:
        # Find the <dt> element with class "result-item"
        dt_elements = search_soup.find_all("dt", class_="result-item")

        for dt_element in dt_elements:

            # Find the <a> element within the <dt> element and extract the href attribute
            course_link = dt_element.find("a")["href"]

            # Construct the full URL
            course_url = f"https://catalog.nau.edu/Courses/{course_link}"

            url_list.append(course_url)

    except AttributeError as e:
        raise e
        return None

    return url_list

def get_class_dict(url_list): # Returns a dictionary of classes

    class_dict = {}

    if url_list:
        for url in url_list:
            course_name, course_description, course_units, course_prerequisites, course_designation, course_semesters = long_lookup(url)

            if course_name and course_description and course_units:
                # Split the string using '&' as delimiter
                split_parts = url.split('?')
                # Loop through the split parts to find and extract the courseId
                course_id = None
                for part in split_parts:
                    if part.startswith("courseId="):
                        course_id_long = part.split('=')[1]
                        course_id = course_id_long.split('&')[0]
                        class_dict[course_id] = [course_name , course_description, course_units, course_prerequisites, course_designation, course_semesters]

    else:
        return None

    return class_dict

def get_class_dict_short(subject, cat_nbr): # Returns a dict of simply course ID and name

    class_dict = {}

    # URL of the search page
    search_url = f"https://catalog.nau.edu/Courses/results?subject={subject}&catNbr={cat_nbr}&term=1237"

    # Send an HTTP GET request to the search page
    search_response = requests.get(search_url)

    # Parse the course page HTML
    search_soup = BeautifulSoup(search_response.content, "html.parser")

    # Find all <a> tags with course details links
    course_links = search_soup.find_all('a', title='view course details')

    # Extract and store course IDs and names in the dictionary
    for link in course_links:
        course_id = link['href'].split('=')[1].split('&')[0]
        course_name = link.get_text(strip=True)
        class_dict[course_id] = course_name

    return class_dict

def long_lookup(course_url):

    # Send an HTTP GET request to the course page
    search_response = requests.get(course_url)

    # Parse the course page HTML
    search_soup = BeautifulSoup(search_response.content, "html.parser")

    # Find the <h2> element and its text
    course_name = search_soup.find("h2").text

    # Find the <strong> element with the text "Description:"
    course_description = search_soup.find("strong", text="Description:").find_next_sibling(text=True).strip()

    # Find the <strong> element with the text "Units:"
    course_units = search_soup.find("strong", text="Units:").find_next_sibling(text=True).strip()

    try:
        course_designation = search_soup.find("strong", text="Requirement Designation:").find_next_sibling(text=True).strip()

    except Exception as e:
        pass
        course_designation = "Unspecified"

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

    return course_name, course_description, course_units, course_prerequisites, course_designation, course_semesters

def random_class(): # generate a random class for funsies

    random_subject = random.choice(name_list)
    url_list = get_urls(random_subject, "")
    random_url = random.choice(url_list)
    course_name, course_description, course_units, course_prerequisites, course_designation, course_semesters = long_lookup(random_url)
    class_dict = get_class_dict([random_url])

    return class_dict

def prereq_tree(input_course_code):

    subject, cat_nbr = get_sub_nbr(input_course_code)
    url_list = get_url_list(subject, cat_nbr)

    if url_list:
        course_url = url_list[0]

        # START WITH ONE CLASS, FIND THE PREREQUS
        # FOR EVERY PREREQ, CHECK THOSE PREREQUS
        # KEEP THEM IN A LIST

        # Send an HTTP GET request to the course page
        search_response = requests.get(course_url)

        # Parse the course page HTML
        search_soup = BeautifulSoup(search_response.content, "html.parser")

        prereq_search = [
        "Prerequisite:",
        "Prerequisite or Corequisite:",
        "Prerequisite or Corequisite: ",
        "Pre- or Corequisite:",
        ]

        try:
            course_prerequisites = search_soup.find("strong", text="Prerequisite:").find_next_sibling(text=True).strip()
        except Exception as e:
            course_prerequisites = None

    else:
        print("No exist")
