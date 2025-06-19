from classes.DatabaseHandler import DatabaseHandler, Course, Section

url = "https://www7.nau.edu/pair/reports/ClassDistribution"

def _example():

    db = DatabaseHandler("database/test.db")

    #db.web_update()

    resp = db.retrieve(Course, {"sub":"CS", "nbr":126, "ending":"L"})

    print(resp)

    for course in resp:

        id = course.id

        sections = db.retrieve(Section, {"id":id}, join_course=True)
        
        print("Entry:", end="")
        print(sections)
        print()

    print(resp)


def _example_2():

    def decrease_term( term_value, semesters=1):
        # Extract year and season code from term value
        year = int("20" + term_value[1:3])  # Convert the 2-digit year to a 4-digit year
        season_code = int(term_value[3])

        season_order = [1, 4, 7, 8]  # Order of seasons by code

        # Calculate the total semesters to decrease
        total_decrease = semesters
        current_index = season_order.index(season_code)

        while total_decrease > 0:
            # Move to the previous season
            current_index -= 1
            if current_index < 0:  # If wrapping around to the previous year
                current_index = len(season_order) - 1
                year -= 1
            total_decrease -= 1

        # Get the new season code
        new_season_code = season_order[current_index]

        # Construct the new term value
        new_term_value = "1" + str(year)[2:] + str(new_season_code)
        return new_term_value
    
    print( decrease_term("1201") )
    
_example_2()