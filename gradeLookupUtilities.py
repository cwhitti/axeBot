import requests
import urllib3
import ssl
from bs4 import BeautifulSoup
from courseClass import Course
from botUtilities import *

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def example():
    page = requestsget("https://www.kompas.com/ramadhan/jadwal-imsakiyah/kota-pangkal-pinang")
    soup = BeautifulSoup(page.text,"lxml")
    options = soup.find("select",{"name":"state"}).findAll("option")
    daerah = []
    for i in options:
        name = i.text
        link = i["value"];

        daerah.append({
              "province": name,
              "link": link
          })

    print(daerah)

def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

def resp_200( resp ):
    return resp.status_code == 200

def get_soup( resp):
    return BeautifulSoup(resp.content, 'html.parser')

def get_grades( search ):

    term = search.sms_code
    classSub = search.sub
    classNbr = search.cat_nbr
    classCode = classSub + " " + classNbr

    url = "https://www7.nau.edu/pair/reports/ClassDistribution"

    # Send GET request to get initial page
    session = get_legacy_session()

    # Send a POST request with form data
    response = session.post( url )

    # Check if the request was successful
    if not resp_200( response ):
        print("Bad!")
        return []

    # Parse the HTML content

    soup = get_soup(response)

    # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
    view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')


    # Prepare the payload with updated form data and the extracted values
    payload = {
        "__VIEWSTATE": view_state,
        "__EVENTVALIDATION": event_validation,
        "ctl00$MainContent$TermList": term,  # Fall 2023
    }

    response = session.post(url, data=payload)

    if not resp_200( response ):
        print("Bad!")
        return []

    soup = get_soup(response)


    try:
        # Extract the __VIEWSTATE and __EVENTVALIDATION values from the page
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

    except AttributeError:

        search.search_szn, search.search_year = decrease_term( search )

        term = get_sms_code(search)
        search.sms_code = term

        print(f"Trying with term {term}")

        get_grades( search )

    if (event_validation != None):

        print(event_validation)
        # Prepare the payload with updated form data and the extracted values
        payload = {
            "__VIEWSTATE": view_state,
            "__EVENTVALIDATION": event_validation,
            "ctl00$MainContent$TermList": term,  # Fall 2023
            "ctl00$MainContent$SubjectList": classSub,  # Example subject, change as needed
            "ctl00$MainContent$Button1": "Submit"
        }

        response = session.post(url, data=payload)

        if not resp_200( response ):

            print("Bad!")
            return []

        soup = get_soup(response)

        entries = soup.find_all('td', class_='small', text=classCode)

        if len(entries) != 0:

            grades = []

            for entry in entries:

                next_siblings = entry.find_next_siblings('td', class_='small', align='right')
                numbers = [sibling.get_text() for sibling in next_siblings]
                grades.append(numbers)

            print(grades)
            return grades

        else:
            print("Bad!")
            return []

def decrease_term( search ):

    szn = search.search_szn
    new_yr = search.search_year

    # fall 2024

    # default to fall
    if szn == "spring" or szn == "winter":

        if szn == "spring":
            new_yr = str( int( new_yr ) - 1)

        new_szn = "fall"

    # default to spring
    else:
        new_szn = "spring"

    return new_szn, new_yr
