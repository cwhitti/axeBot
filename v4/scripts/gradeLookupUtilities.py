from bs4 import BeautifulSoup
import requests
import urllib3
import ssl

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)
        
def _get_legacy_session( self ):
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

def resp_200( resp ):
    return resp.status_code == 200

def get_soup( resp):
    return BeautifulSoup(resp.content, 'html.parser')

# def get_grades( search ):

#     term = search.sms_code
#     classSub = search.sub
#     classNbr = search.cat_nbr
#     endLetter = search.ending
#     classCode = classSub + " " + classNbr + endLetter

#     # Send GET request to get initial page
#     session = get_legacy_session()

#     # Send a POST request with form data
#     response = session.post( url )

#     # Check if the request was successful
#     if not resp_200( response ):
#         return []

#     # Parse the HTML content

#     soup = get_soup(response)

#     # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
#     view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
#     event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')


#     # Prepare the payload with updated form data and the extracted values
#     payload = {
#         "__VIEWSTATE": view_state,
#         "__EVENTVALIDATION": event_validation,
#         "ctl00$MainContent$TermList": term,  # Fall 2023
#     }

#     response = session.post(url, data=payload)

#     if not resp_200( response ):
#         return []

#     soup = get_soup(response)


#     try:
#         # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
#         view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
#         event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

#     except AttributeError:

#         search.search_szn, search.search_year = decrease_term( search )

#         term = get_sms_code(search)
#         search.sms_code = term

#         course_info = get_grades( search )

#         return course_info

#     if (event_validation != None):

#         # Prepare the payload with updated form data and the extracted values
#         payload = {
#             "__VIEWSTATE": view_state,
#             "__EVENTVALIDATION": event_validation,
#             "ctl00$MainContent$TermList": term,  # Fall 2023
#             "ctl00$MainContent$SubjectList": classSub,
#             "ctl00$MainContent$Button1": "Submit"
#         }

#         response = session.post(url, data=payload)

#         if not resp_200( response ):

#             print("Bad :(")
#             return []

#         soup = get_soup(response)

#         entries = []
#         info = soup.find_all('td', string=classCode)

#         for td_tag in info:

#             tr_tag = td_tag.parent  # Get the parent <tr> tag
#             entry = [td.text for td in tr_tag.find_all('td')]
#             entries.append(entry)

#         course_info = []

#         if len(entries) != 0:

#             for entry in entries:

#                 class_name = entry[0]
#                 section = entry[1]
#                 #class_nbr = entry[2]
#                 prof = entry[3]
#                 a = entry[4]
#                 b = entry[5]
#                 c = entry[6]
#                 d = entry[7]
#                 f = entry[8]
#                 au = entry[9]
#                 p = entry[10]
#                 ng = entry[11]
#                 w = entry[12]
#                 i = entry[13]
#                 ip = entry[14]
#                 pen = entry[15]
#                 total = entry[16]

#                 course = Course(class_name, term=term)

#                 course.update_grades( section, prof, a, b, c, d, f, au, p, ng, w,
#                                                                     i, ip, pen, total)

#                 course_info.append(course)

#         return course_info

#     else:
#         return []

# def decrease_term( search ):

#     szn = search.search_szn
#     new_yr = search.search_year

#     # default to fall
#     if szn == "spring":

#         new_yr = str( int( new_yr ) - 1)
#         new_szn = "winter"

#     elif szn == "fall":
#         new_szn = "summer"

#     elif szn == "summer":
#         new_szn = "spring"

#     else:
#         new_szn = "fall"

#     return new_szn, new_yr
