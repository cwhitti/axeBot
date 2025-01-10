import re
from datetime import datetime

class NAUHandler():
        
    def __init__(self) -> None:
        
        self.current_term = None

        self.end_sigs    = ['H','h','L','l','W','w','R','r','c','C']

        self.szn_dict = {
            "Spring":"1",
            "Summer":"4",
            "Fall":"7",
            "Winter":"8"
            }

        self.term_dict = {
            "Spring":"January 10",
            "Summer":"May 10",
            "Fall":"August 10",
            "Winter":"December 10"
        } 
    def decrease_term(self, term_value, semesters=1):
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
    def increase_term(self, term_value, semesters=1):
            # Extract year and season code from term value
            year = int("20" + term_value[1:3])  # Convert the 2-digit year to a 4-digit year
            season_code = int(term_value[3])

            season_order = [1, 4, 7, 8]  # Order of seasons by code

            # Calculate the total semesters to increase
            total_increase = semesters
            current_index = season_order.index(season_code)

            while total_increase > 0:
                # Move to the next season
                current_index += 1
                if current_index >= len(season_order):  # If wrapping around to the next year
                    current_index = 0
                    year += 1
                total_increase -= 1

            # Get the new season code
            new_season_code = season_order[current_index]

            # Construct the new term value
            new_term_value = "1" + str(year)[2:] + str(new_season_code)
            return new_term_value
    
    def is_current_term( self, term ):
        return int(term) == int( self.calculate_current_term() )
    
    def calculate_current_term( self ):

        # Get today's date
        today = datetime.now()

        # Convert term_dict dates to datetime objects with the current year
        season_dates = {
            season: datetime.strptime(f"{today.year}-{date}", "%Y-%B %d")
            for season, date in self.term_dict.items()
        }

        # Determine the current season
        current_season = None
        for season, date in sorted(season_dates.items(), key=lambda x: x[1]):
            if today >= date:
                current_season = season
        if today < season_dates["Spring"]:  # Special case for Winter crossing year boundary
            current_season = "Winter"
            current_year = today.year - 1
        else:
            current_year = today.year

        # Mapping seasons to numerical values
        szn_dict = {
            "Spring": "1",
            "Summer": "4",
            "Fall": "7",
            "Winter": "8"
        }

        # Generate the term value
        term_value = "1" + str(current_year)[2:] + szn_dict[current_season]
        return term_value

    def calculate_set_term( self, season, year):

        # Normalize the season input
        season = season.capitalize()

        # Validate the input season
        if season not in self.szn_dict:
            return None
            #raise ValueError("Invalid season. Valid options are: Spring, Summer, Fall, Winter.")

        # Generate the term value
        term_value = "1" + str(year)[2:] + self.szn_dict[season]
        return term_value

    def calculate_year_and_season(self, term=None):
        
        # recurse back if no term value
        if term ==  None:

            # calculate current term
            term = self.calculate_current_term()
            return self.calculate_year_and_season( term )
        
        # Mapping season codes to names
        code_to_season = {
            "1": "Spring",
            "4": "Summer",
            "7": "Fall",
            "8": "Winter"
        }

        # Extract year and season code from the term value
        year_prefix = "20"
        year = int(year_prefix + term[1:3])  # Convert the 2-digit year to a 4-digit year
        season_code = term[3]

        # Get the season name
        season = code_to_season.get(season_code, "Unknown season")

        # return the season and year
        return season, year
    
    def parse_course_code( self, string ):

            match = re.match(r"([A-Z]+)\s*(\d+)([A-Z]*)", string)
            if match:
                return match.groups()
            else:
                return None
    
    