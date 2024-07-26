import discord 
from datetime import datetime
from classes.CourseClass import Course

class myEmbed:
    '''
    PUBLIC FUNCTIONS
    '''

    def embed_grades( self, embed, search, courses:list ):

        CHAR = '.'
        WIDTH = 98

        for course in courses:

            #print(f"HELLOOOOOOO, {course.name}")

            #course.debug()

            name = course.name
            szn = search.szn.capitalize()
            year = search.year
            section = course.section
            prof = course.prof
            A = int(course.grades["A"])
            B = int(course.grades["B"])
            C = int(course.grades["C"])
            D = int(course.grades["D"])
            F = int(course.grades["F"])
            # AU = int(course.grades["AU"])
            P = int(course.grades["P"])
            # NG = int(course.grades["NG"])
            W = int(course.grades["W"])
            # I = int(course.grades["I"])
            # IP = int(course.grades["IP"])
            # pen = int(course.grades["pen"])
            total =int(course.grades["total"])

            # embed.title = f"{name} Section {section} Grade Distribution"

            # #embed.add_field(name=f"{DESIGN1 * X_CHR} Class Info {DESIGN1 * X_CHR}", value="", inline=False)
            # #embed_section_title(embed, WIDTH, CHAR, "Class Info")
            # embed.add_field(name="Professor", value=prof, inline=True)
            # embed.add_field(name="Term", value=f"{szn} {year}", inline=False)
            # embed.add_field(name="Section", value=section, inline=False)

            dropped = ( W / total ) * 100

            # Check if pass/fail
            if ( A + B + C + D == 0 ):

                passed = (P / total) * 100
                failed = (100 - passed - dropped)

                # account for rounding errors
                if failed < 0:
                    failed = 0

            # graded class
            else:

                passed_sum = A + B + C
                passed = (passed_sum / total) * 100
                failed = (100 - passed - dropped)

            # embed.add_field(name="",
            #             value="",
            #             inline=False)
            # embed.add_field(name="Passed",
            #                 value="✅ "  + str( round( passed, 2 ) ) + "%",
            #                 inline=True)
            # embed.add_field(name="",
            #                 value="_\* Passing grades are counted as A, B, C_",
            #                 inline=True)
            # embed.add_field(name="Dropped",
            #                 value="⚠️ "  + str( round( dropped, 2 ) ) + "%",
            #                 inline=False)
            # embed.add_field(name="Failed ",
            #                 value="🛑 "  + str( round( failed, 2 ) ) + "%",
            #                 inline=False)
            # #embed_section_title(embed, WIDTH, CHAR, "Class Grades")

            # text = ""

            # embed.add_field(name=f"",
            #                 value=f'''
            #                 **{total} Total Enrolled**

            #                 ''',
            #                 inline=False)

            # if ( A + B + C + D != 0 ):
            #     self._add_grade(embed, text + "A", course.grades["A"])
            #     self._add_grade(embed, text + "B", course.grades["B"])
            #     self._add_grade(embed, text + "C", course.grades["C"])
            #     self._add_grade(embed, text + "D", course.grades["D"])
            #     self._add_grade(embed, text + "F", course.grades["F"])
            #     self._add_grade(embed, text + "W", course.grades["W"])

            # else:

            #     self._add_grade(embed, text + "P", course.grades["P"])
            #     self._add_grade(embed, text + "F", course.grades["F"])
            #     self._add_grade(embed, text + "W", course.grades["W"])

            return

        embed.set_footer(text=f"Based on {szn} {year} records.")
        embed.set_thumbnail(url="https://i.pinimg.com/564x/4a/25/80/4a25805f04f4ba694d9fff4a41426799.jpg")


    def embed_course( self, embed, course, search ):

        course_name = course.title
        course_description = course.desc
        course_units = course.units
        course_designation = course.desig
        course_semesters = course.offered
        course_id = course.courseID
        course_url = course.url2
        course_prereqs = course.prereqs
        course_cat = search.year
        szn = search.szn

        embed.title = course_name

        embed.add_field(name="Course ID:",
            value=course_id,
            inline=False)
        embed.add_field(name="Description:",
            value=course_description,
            inline=False)
        embed.add_field(name="Units:",
            value=course_units,
            inline=False)
        embed.add_field(name="Current Offerings:",
            value=course_semesters,
            inline=False)
        embed.add_field(name="Prerequisites:",
            value=course_prereqs,
            inline=False)
        embed.add_field(name="Requirement Designation:",
            value=course_designation,
            inline=False)
        embed.add_field(name="",
            value=f"[Course Link]({course_url})",
            inline=False)

        embed.set_footer(text=f"Based on {szn.capitalize()} {course_cat} catalogue")

    def get_formatted_time( self ):
        # Get the current datetime
        now = datetime.now()

        # Format the datetime object
        formatted_now = now.strftime("%B %d, %Y – %-I:%M%p")

        # Adjusting the format to match the required output
        formatted_now = formatted_now.replace("AM", "am").replace("PM", "pm")

        return formatted_now

    def initialize_embed( self, title="", desc="", color="" ):

        embed = discord.Embed( title=title, 
                                description=desc,
                                color=color)
        return embed

    def set_img( self, img_url, embed ):
        embed.set_image( url = img_url)

    '''
    PRIVATE FUNCTIONS
    '''

    def __init__(self) -> None:

        self.title = None
        self.desc = None

    def _add_grade(self, embed, text, grade):

        str = f"{text}: {grade}"

        embed.add_field(name=str, value="")