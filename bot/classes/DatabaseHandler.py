from secret import url
from classes.SQLHandler import SQLHandler, Course, Section
from classes.MyWebHandler import MyWebHandler

class DatabaseHandler( MyWebHandler, SQLHandler ): 

    def __init__(self, db_path, end_szn="Spring", end_year="2003", dbg=False, reset_db=False, ) -> None:

        # initialize variables
        self.db_path = db_path
        self.dbg = dbg
        self.reset_db = reset_db


        # Initialize inherited classes
        SQLHandler.__init__(self, self.db_path, self.dbg, reset_db)
        MyWebHandler.__init__( self )

        # Other specific variables
        self.end_term = self.calculate_set_term(end_szn, end_year)

    def add_all_courses( self, term, end_term=None ):

        # assign end term if none
        if end_term == None:
            end_term = self.end_term

        # iterate through the semesters
        if int(term) >= int(end_term):
            
            # add courses for that term
            self.add_courses( term ) 

            # Decrease term
            term = self.decrease_term( term )
            
            # recursively add courses
            return self.add_all_courses( term, end_term=end_term )
        
        # Return True
        return True

    def add_courses( self, term ):

        # initialize variables
            # None

        # Get subjects from catalog; Not actually available so we use subjects from grades
        subjects = self.get_subjects( term )

        # calculate season and year
        season, year = self.calculate_year_and_season( term )

        # iterate through subjects
        for subject in subjects:
                
            # Get course info
            course_ids = self.get_course_ids( subject, term )
            
            # debug print
            if self.dbg:
                print(f"[{season} {year} Courses] Inserting {subject} ({len(course_ids)} items)")

            # iterate through
            for search_code, course_id in course_ids.items():
                
                # Create a new course object
                course = self.create_course( course_id, search_code, term, season, year  )

                # Insert the object
                self.add_course( course )

    def add_course( self, course:Course ):
        self.insert( course )

    def add_all_sections( self, term, end_term = None ):
        # assign end term if none
        if end_term == None:
            end_term = self.end_term

        # iterate through the semesters
        if int(term) >= int(end_term):
            
            # add courses for that term
            self.add_sections( term ) 

            # Decrease term
            term = self.decrease_term( term )
            
            # recursively add courses
            return self.add_all_sections( term, end_term=end_term )
        
        # Return True
        return True

    def add_sections( self, term ):

        # Get subjects from catalog; Not actually available so we use grades
        subjects = self.get_subjects( term )

        # calculate season and year
        season, year = self.calculate_year_and_season( term )

        # iterate through subjects
        for subject in subjects:

            # Get grade data for this term
            courses = self.get_grade_data(term, subject)

            # debug print
            if self.dbg:
                print(f"[{season} {year} Sections] Inserting {subject} ({len(courses)} items)")

            # Iterate through courses
            for course in courses:
                
                # get the search code
                search_code = course[0]

                # grab the id
                id = self.retrieve_course_id( search_code, term )

                # ensure ID != None
                if id != None:

                    # create a new section
                    section = self.create_section(id, term, course)

                    # insert the section
                    self.add_section( section )
                else:
                    print("Course not found in database")
    def add_section( self, section:Section ):
        self.insert( section )

    def create_course( self, course_id, search_code, term, season, year ):

        # Format data on the course
        subject, nbr, ending = self.parse_course_code( search_code )

        # return course
        return Course(      
                        id=course_id,
                        term=term,
                        season=season,
                        year=year,
                        sub=subject,
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

    def custom_query( self, model_str, filters):

        if model_str == "section":
            model = Section

        if model_str == "course":
            model = Course 
        return self.retrieve( model, filters, join_course=True)
        
    def find_sections( self, filters ):
        return self.retrieve( Section, filters )

    def find_courses( self, filters ):
        return self.retrieve( Course, filters )
        
    def get_course_ids( self, subject, term ):

        soup = self.get_nau_catalog(subject, term)
        
        return self.format_class_codes( soup )
    
    def get_grade_data( self, term, subject ):
            
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
                if row_data[0] != "Class":
                    data.append(row_data)
        
        return data
    
    def retrieve_course_id( self, search_code, term ): 
        
        # initialize variables
        id = None 
        filters = {"search_code":search_code, "term":term}
        
        # retrieve records 
        records = self.retrieve( Course, filters=filters )

        # check if one record was chosen
        if len( records ) == 1:

            # grab the one record
            record = records[0]

            # grab the id
            id = record.id

        # return the id
        return id

    def retrieve_highest_term( self, modelStr:str ):
        '''
        Retrieves the highest term from model
        '''
        max_term = None

        if modelStr == "Course":
            model = Course

        elif modelStr == "Section":
            model = Section
        
        else:
            assert("A model most be chosen for retrieve_highest_term()")
        records = self.retrieve( model )

        if len( records ) > 0:
            max_term = max(record.term for record in records if hasattr(record, 'term'))

        return max_term
    
    def retrieve_sections( self, id, term=None, section=None, join_course = False ):

        # initialize variables
        filters = {
                "id":id
        }

        # check if a term was added
        if term != None:

            # add in term filter
            filters["term"] = term
            
        # NOT SUPPORTED BY _parse_msg CURRENTLY:
        # Filter by section if included in search
        if section != None:
            filters["section"]=section

        # search in db
        records = self.retrieve( Section, filters, join_course=join_course )

        # return records
        return records

    def retrieve_unique_subjects( self, model, term=None  ):

        '''
        Retrieves all unique subjects from the database. Can be filtered by term
        '''

        filters = {}
        subjects = None

        if term != None:
            filters["term"] = term


        records = self.retrieve(model, filters)

        if len( records ) > 0:

            # Extract unique subjects
            subjects = list({course.subject for course in records})

        return subjects

    async def web_update( self ):

        '''
        Add the newest term to the dataset if data is available
        '''
        # initialize variables
            # None

        # Calculate current term
        # current_term = self.calculate_current_term()
        # last_term = self.decrease_term( current_term )

        # Open session
        self.open_session()

        # Get most recent terms from nau
            # function: self.calculate_current_term()
        catalog_term = self.get_latest_term( "Catalog" )
        grades_term  = self.get_latest_term( "Grades" )

        # Get most recent terms from my db
        last_catalog_term = self.retrieve_highest_term( "Course" )
        last_grades_term = self.retrieve_highest_term( "Section" )

        # # Begin adding courses for this current term
        # if last_catalog_term == None :
        #     self.add_all_courses( term = current_term, 
        #                             #end_term = self.decrease_term(current_term) 
        #                         )    

        # Begin adding grades for the term before
        # if last_grades_term == None:
        #     self.add_all_sections( term = current_term,
        #                             #end_term = self.decrease_term(last_term)
                                # )

        # Check Courses table to add new courses in
        if int( catalog_term ) > int( last_catalog_term ):
            # Add the term
            self.add_courses( catalog_term )
        
        # Check Section table to add new sections in
        if int( grades_term ) > int( last_grades_term ):
            # add the grades
            self.add_sections( grades_term )  

        print("Finished updating database")  
