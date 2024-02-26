import re
import classUtilities as cls
import requests
from courseClass import Course
from bs4 import BeautifulSoup

def create_search_url( axeBot ):

    base_url = "https://catalog.nau.edu/Courses/results?"
    subject = "subject=" + axeBot.sub
    cat_nbr = "&catNbr=" + axeBot.cat_nbr + axeBot.ending
    term="&term=" + axeBot.sms_code

    url = base_url + subject + cat_nbr + term

    return url
    #return f"https://catalog.nau.edu/Courses/results?subject={subject}&catNbr={cat_nbr}&term={semester_code}"

def correct_start( arg1, name_list ):

    matches = re.findall(r'[A-Za-z]+|\d+', arg1)

    letters = matches[0]

    # fail out if arg[1] does not startwith in name list
    for name in name_list:
        if letters == name:
            return True

    return False

def get_class_dict( axeBot ): # Returns a list of classes

    # initialize variables
    url_list = axeBot.url_list
    course_list = []
    desc = None
    units = None
    desig = None
    sems = None

    # ensure urls
    if url_list:

        #loop thru URLS
        for url in url_list:

            #get search soup
            search_soup = cls.get_search_soup(url)

            # get name, ID
            name = cls.get_course_name(search_soup)
            id = cls.get_course_id(url)

            # get class elements
            desc = cls.get_course_description(search_soup)
            units = cls.get_course_units(search_soup)
            desig = cls.get_course_designation(search_soup)
            sems = cls.get_course_semesters(search_soup)

            # create instance
            course = Course( name, desc, units, desig, sems,
                                            id, axeBot.sms_code, url)

            # add instance to list
            course_list.append(course)

    return course_list

def get_class_dict_short( search ):

    course_list = []
    desc = None
    units = None
    desig = None
    sems = None
    url = None

    # Parse the course page HTML
    search_soup = get_search_soup( search.search_url )

    # Find all <a> tags with course details links
    course_links = search_soup.find_all('a', title='view course details')

    # Extract and store course IDs and names in the dictionary
    for link in course_links:

        id = link['href'].split('=')[1].split('&')[0]
        name = link.get_text(strip=True)
        course = Course(name, desc, units, desig, sems,
                                        id, search.sms_code, url)
        course_list.append( course )

    return course_list

def get_search_soup(search_url):

    # Send an HTTP GET request to the search page
    search_response = requests.get(search_url)

    # Parse the search page HTML
    search_soup = BeautifulSoup(search_response.content, "html.parser")

    return search_soup

def get_sms_code(axeBot):

    # initialize variables
    dict = axeBot.szn_dict
    szn = axeBot.search_szn
    year = axeBot.search_year
    dig_1 = "1"

    # check for valid year
    if ( int(year) > 2005 ):

        # use the custom bits
        dig_2 = year[2]
        dig_3 = year[3]

    # not a valid year
    else:

        # use the default bits
        dig_2 = axeBot.dft_year[ 2 ]
        dig_3 = year.dft_year[ 3 ]

    # check for correct season
    if ( szn in dict.keys() ):

        # use the custom bits
        dig_4 = dict[ szn ]

    # invalid season
    else:
        # use the default szn
        dig_4 = dict[ axeBot.dft_szn ]

    return dig_1 + dig_2 + dig_3 + dig_4

def get_sub_nbr(axeBot):

    # initialize variabbles
    cmb_str = axeBot.search_code
    endings = axeBot.end_sigs
    course_code = cmb_str.upper()
    extract = course_code

    if course_code[-1] in endings: # there are endings

        axeBot.ending += course_code[-1]

        # get rid of the ending
        extract = extract[:-1]

        if course_code[-2] in endings:

            axeBot.ending += course_code[-2]

            # get rid of second ending
            extract = extract[:-1]

    # handle "CS249"
    matches = re.findall(r'[A-Za-z]+|\d+', extract)

    # Ensure matches contains exactly 2 items
    matches += [''] * (2 - len(matches))

    return matches[0], matches[1]
