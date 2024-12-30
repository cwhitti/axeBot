def get_course_name(search_soup):
    return search_soup.find("h2").text

def get_course_description(search_soup):

    course_description = search_soup.find("strong", text="Description:").find_next_sibling(text=True).strip()

    # shorten if too long
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
        course_designation = "Unspecified"

    return course_designation

def get_course_offered(search_soup):

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
