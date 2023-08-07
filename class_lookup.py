import requests
from bs4 import BeautifulSoup

def get_url_list(input_course_code):

    print("Parsing the following from discord: ", input_course_code)

    course_code = input_course_code.replace(" ","")

    end_signifiers = ['H','h','L','l','W','w','R','r']

    if course_code[-1] in end_signifiers:
    # check length of string, assign accordingly
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
            subject = '123456789'
            cat_nbr = 'xxxxxxxxx'

    else:
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
            subject = '123456789'
            cat_nbr = 'xxxxxxxxxx'

    try: #validates that subject is a string  and catnbr has 3 numbers, may be invalid
        str(subject)
        if cat_nbr[-1] in end_signifiers:
            int(cat_nbr[:3])
            upper_nbr = cat_nbr[:-1] + cat_nbr[-1].upper()
            cat_nbr = upper_nbr
        else:
            int(cat_nbr)

    except ValueError:
        return None

    upper_subject = subject.upper()

    url_list = get_urls(upper_subject, cat_nbr)

    return url_list

def get_urls(subject, cat_nbr):

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

def get_class_dict(url_list):

    class_dict = {}

    if len(url_list) > 0:
        for url in url_list:
            course_name, course_description, course_units, course_prerequisites = find_class(url)

            if course_name and course_description and course_units:
                # Split the string using '&' as delimiter
                split_parts = url.split('?')
                # Loop through the split parts to find and extract the courseId
                course_id = None
                for part in split_parts:
                    if part.startswith("courseId="):
                        course_id_long = part.split('=')[1]
                        course_id = course_id_long.split('&')[0]
                        class_dict[course_id] = [course_name , course_description, course_units, course_prerequisites]

    else:
        print("dont exist")
        return None

    return class_dict


def find_class(course_url):

    # Send an HTTP GET request to the course page
    course_response = requests.get(course_url)

    # Parse the course page HTML
    course_soup = BeautifulSoup(course_response.content, "html.parser")

    course_name = course_soup.find("h2").text

    # Find the <strong> element with the text "Description:"
    course_description = course_soup.find("strong", text="Description:").find_next_sibling(text=True).strip()

    # Find the <strong> element with the text "Units:"
    course_units = course_soup.find("strong", text="Units:").find_next_sibling(text=True).strip()

    prereq_search = [
    "Prerequisite:",
    "Prerequisite or Corequisite:",
    "Prerequisite or Corequisite: ",
    "Pre- or Corequisite:",
    "Corequisite:"
    ]

    for phrase in prereq_search:
        try:
            course_prerequisites = course_soup.find("strong", text=phrase).find_next_sibling(text=True).strip()

            if course_prerequisites:
                extracted_text = " ".join(phrase.split()[:-1])
                course_prerequisites = course_prerequisites + (f" - ({extracted_text})")
                break

        except Exception as e:
            pass
            course_prerequisites = None

    return course_name, course_description, course_units, course_prerequisites


def prereq_tree(input_course_code):

    url_list = get_url_list(input_course_code)
    print(url_list)

    if url_list:
        course_url = url_list[0]

        # START WITH ONE CLASS, FIND THE PREREQUS
        # FOR EVERY PREREQ, CHECK THOSE PREREQUS
        # KEEP THEM IN A LIST

        # Send an HTTP GET request to the course page
        course_response = requests.get(course_url)

        # Parse the course page HTML
        course_soup = BeautifulSoup(course_response.content, "html.parser")

        prereq_search = [
        "Prerequisite:",
        "Prerequisite or Corequisite:",
        "Prerequisite or Corequisite: ",
        "Pre- or Corequisite:",
        ]

        try:
            course_prerequisites = course_soup.find("strong", text="Prerequisite:").find_next_sibling(text=True).strip()
            if course_prerequisites in prereq_search:
                print(course_prerequisites)
        except Exception as e:
            course_prerequisites = None

        print(course_prerequisites)

    else:
        print("No exist")
