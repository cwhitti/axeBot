import requests
from bs4 import BeautifulSoup

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

    # Find the <strong> element with the text "Units:"
    try:
        course_prerequisites = course_soup.find("strong", text="Prerequisite:").find_next_sibling(text=True).strip()

    except AttributeError:
        try:
            course_prerequisites = course_soup.find("strong", text="Pre- or Corequisite:").find_next_sibling(text=True).strip()

        except Exception as e:
            course_prerequisites = None

    return course_name, course_description, course_units, course_prerequisites

def get_class_dict(input_course_code):

    course_code = input_course_code.replace(" ","")
    class_dict = {}

    if course_code[-1] == 'H':
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
            subject = 0
            cat_nbr = 0

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
            subject = 0
            cat_nbr = 0

    try:
        str(subject)
        if cat_nbr[-1] == 'H':
            check_len = len(cat_nbr) - 3
            int(cat_nbr[:check_len])
        else:
            int(cat_nbr)

    except ValueError:
        return class_dict

    upper_subject = subject.upper()
    url_list = get_urls(upper_subject, cat_nbr)

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

    return class_dict
