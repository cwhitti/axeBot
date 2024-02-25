import re
import classUtilities as cls
import requests
from courseClass import Course

def create_search_url( axeBot ):

    base_url = "https://catalog.nau.edu/Courses/results?"
    subject = "subject=" + axeBot.sub
    cat_nbr = "&catNbr=" + axeBot.cat_nbr + axeBot.ending
    term="&term=" + axeBot.sms_code

    url = base_url + subject + cat_nbr + term

    return url
    #return f"https://catalog.nau.edu/Courses/results?subject={subject}&catNbr={cat_nbr}&term={semester_code}"

def get_class_dict( axeBot, type ): # Returns a list of classes

    # initialize variables
    url_list = axeBot.url_list
    course_list = None
    desc = None
    units = None
    desig = None
    sems = None

    # ensure urls
    if url_list:

        course_list = []

        #loop thru URLS
        for url in url_list:

            #get search soup
            search_soup = cls.get_search_soup(url)

            # get name, ID
            name = cls.get_course_name(search_soup)
            id = cls.get_course_id(url)

            # check for long form
            if ( type != "short" ):

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

def get_class_dict_short(subject, cat_nbr, semester_code):

    class_dict = {}

    # URL of the search page
    search_url = create_search_url(subject, cat_nbr, semester_code)

    # Parse the course page HTML
    search_soup = get_search_soup(search_url)

    # Find all <a> tags with course details links
    course_links = search_soup.find_all('a', title='view course details')

    # Extract and store course IDs and names in the dictionary
    for link in course_links:
        course_id = link['href'].split('=')[1].split('&')[0]
        course_name = link.get_text(strip=True)
        class_dict[course_id] = course_name

    return class_dict

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

    return matches[0], matches[1]
