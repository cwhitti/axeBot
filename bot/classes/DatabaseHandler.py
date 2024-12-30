import re
from secret import url
from classes.SQLHandler import SQLHandler, Course, Section
from classes.MyWebHandler import MyWebHandler

class DatabaseHandler( MyWebHandler, SQLHandler ): 

    def __init__(self, db_path, end_szn="Spring", end_year="2003", dbg=False ) -> None:

        # initialize variables
        self.db_path = db_path
        self.dbg = dbg

        # Initialize inherited classes
        SQLHandler.__init__(self, self.db_path, self.dbg)
        MyWebHandler.__init__(self)

        # Other specific variables
        self.end_term = self.calculate_set_term(end_szn, end_year)

    def get_course_ids( self, term, subject ):

        response = self.get_nau_catalog(subject, nbr="", term=term, ending="")

        soup = self.get_soup( response )
        
        return self.format_class_codes( soup )
    
    def get_highest_term( self ):

        records = self.retrieve( Course )
        max_term = max(record.term for record in records if hasattr(record, 'term'))

        return max_term
    
    def get_term_data( self, term, subject ):
            
        # initialize variables 
        data = []

        # send subject post
        response = self.post_subject(term, subject)

        # get soup
        soup = self.get_soup(response)

        # Find all rows in the table
        rows = soup.select("#MainContent_GridView1 tr, #MainContent_GridView2 tr")

        # Extract and print the data from each row
        for row in rows:
            columns = row.find_all("td")
            if columns:
                row_data = [col.get_text(strip=True) for col in columns]
                data.append(row_data)
        
        return data
    
    def create_course( self, term, season, year, data ):

        def extract_suffix( string ):

            match = re.search(r'[A-Za-z]+$', string)
            return match.group(0) if match else ''

        # initialize variables
        term: int = term

        # info from the data
        search_code: str = data[0]

        # extracted info
        sub:  str = search_code.split()[0]
        nbr:  str = search_code.split()[1]

        ending: str = extract_suffix(nbr)
        nbr = nbr.strip(ending)

        # Finally, get course id
        course_id: str = data[17]
        
        # return course
        return Course(      
                        id=course_id,
                        term=term,
                        season=season,
                        year=year,
                        sub=sub,
                        nbr=nbr,
                        ending=ending,
                        search_code=search_code,
                    )
    
    def create_section( self, course_id, term, data ):

        course_id: str = course_id
        section: str = data[1]
        instructor: str = data[3]
        A: int = data[4]
        B: int = data[5]
        C: int =data[6]
        D: int = data[7]
        F: int = data[8]
        AU: int = data[9]
        P: int = data[10]
        NG:  int =data[11]
        W: int = data[12]
        I: int = data[13]
        IP: int = data[14]
        Pending: int = data[15]
        Total: int = data[16]

        return Section( id=course_id,
                        section=section,
                        term=term,
                        instructor=instructor,
                        A=A,
                        B=B,
                        C=C,
                        D=D,
                        F=F,
                        AU=AU,
                        P=P,
                        NG=NG,
                        W=W,
                        I=I,
                        IP=IP,
                        Pending=Pending,
                        Total=Total
        )

    def find_sections( self, filters ):
        return self.retrieve( Section, filters )

    def find_courses( self, filters ):
        return self.retrieve( Course, filters )

    def web_update( self ):

        # Initialize variables
        previous_code = ""
        current_code = ""

        # Get current term at NAU (in NAUHandler)
            # function: self.calculate_term()
        term = self.calculate_current_term()

        # Create new web session
            # function: self.open_session()
        self.open_session()

        # Begin iterating through semesters
        while int(term) >= int(self.end_term):

            # Check if term is in database
            if not self.check_exists(Course, {"term": term} ):

                # Get all subjects for term
                subjects = self.get_subjects( term )

                # grab season and year
                season, year = self.calculate_year_and_season(term)

                # iterate throughe each subject 
                for subject in subjects:

                    # Get term data for that subject
                    courses = self.get_term_data( term, subject ) 

                    # Get course IDs
                    course_IDs = self.get_course_ids( term, subject )

                    # iterate through each course
                    for course_data in courses:
                        
                        # get course code 
                        current_code = course_data[0]
                        
                        # Ignore anything that doesn't have a corresponding id at NAU
                        if current_code not in course_IDs.keys():
                            continue

                        # Save the course ID
                        course_data.append(course_IDs[current_code])
                        
                        # If course code doesn't look like the one before it, make a new course
                        if current_code != previous_code:
                            
                            # Make the new course
                            new_course = self.create_course( term, season, year, course_data )

                            # insert it into the database, with refresh
                            self.insert( new_course, refresh=True )
                            
                            # reset the previous code
                            previous_code = current_code

                        # record this section
                        new_section = self.create_section( new_course.id, term, course_data )

                        # Insert the section
                        self.insert( new_section )

                    # end for loop - course list
                # end for loop - subject list
            # end database check

            # decrease the term
            term = self.decrease_term( term, 1 )
                        
        # end while loop