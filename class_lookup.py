import requests
from bs4 import BeautifulSoup


def search_class(subject, cat_nbr):

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

def main():

    # User input for the course code
    input_course_code = input("Enter the course code (e.g. STA371): ")
    course_code = input_course_code.replace(" ","")

    # check length of string, assign accordingly
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
        int(cat_nbr)

    except ValueError:
        print("Course does not exist.")
        return 0

    url_list = search_class(subject, cat_nbr)

    if len(url_list) > 0:
        for url in url_list:
            course_name, course_description, course_units, course_prerequisites = find_class(url)
            if course_name and course_description and course_units:
                # Print the extracted information
                print()
                print("Course Name:",course_name)
                print("\tCourse Description:", course_description)
                print("\tCourse Units:", course_units)
                print("\tCourse Prerequisites:",course_prerequisites)

    else:
        print("Course does not exist.")
    return 0
