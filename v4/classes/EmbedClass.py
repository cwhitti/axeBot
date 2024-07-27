import discord 
import config as cfg
from secret import PREFIX
import scripts.pieChart as pc
from datetime import datetime
from classes.CourseClass import Course


class myEmbed:
    '''
    PUBLIC FUNCTIONS
    '''

    def embed_grades( self, embed, search, courses:list ):
        
        profs = {}
        
        desc = ""

        for course in courses:
            details = self.embed_course_grades( course, search)

            if len(details) + len(desc ) <= 4000:

                desc += details
            
            else:
                desc += "```Omitted 1 Class```"

        # desc += "```  CLASS DESTRIBUTION   ```"
        # desc += f'''
        # _*Passing grades are counted as A, B, C_
        # '''

        if len( desc) < 4096:
            embed.description = desc
        
        else:
            embed.description = "```ERROR: Too many classes to display!```"

        embed.set_footer(text=f"Based on the {search.szn.capitalize()} {search.year} catalog")

        filename = cfg.PIE_CHART_FILE

        pc.create_figure( filename, search, courses)


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

    def embed_course_grades( self, course, search, ):

        details = f''''''

        if course.grades["P"] != '0':

            passed = int(course.grades["P"])
            failed = int(course.grades["F"])
            w = int(course.grades["W"])
            total = int(course.grades["total"])

            pct_pass = round((passed / total) * 100, 2)
            pct_fail = round((failed / total) * 100, 2) 
            pct_w = round((w / total) * 100, 2)

        else:
            a = course.grades["A"]
            b = course.grades["B"]
            c = course.grades["C"]
            d = course.grades["D"]
            f = course.grades["F"]
            w = course.grades["W"]
            total = course.grades["total"]

            passed = int(a) + int(b) + int(c)
            failed = int(d) + int(f)

            total = int(total)
            w = int(w)
            
            pct_pass = round((passed / total) * 100, 2)
            pct_fail = round((failed / total) * 100, 2) 
            pct_w = round((w / total) * 100, 2)


        details += \
        f'''
        **Section {course.section} - {course.prof}**
            ```
✅ {pct_pass}% Passed
🚸 {pct_w}% Dropped
🛑 {pct_fail}% Failed
👥 {total} Enrolled ```
            '''

        return details 
    
    def embed_subject( self, embed, courses:list ):
    
        desc = f"\n**Listing {len(courses)} courses:\n**"

        embed.description = desc

        for coursename in courses:

            words = coursename.split()
            desc += f"• {words[0]} {words[1]}\n"

        # while index < len( courses ):
            
        #     # empty chunk
        #     chunk = ""

        #     # check for good to add
        #     if len( chunk ) + len( courses[index] ) < 4096 and embedlen < 6000:

        #         # words = coursename.split()
        #         # desc += f"• {words[0]} {words[1]}\n"

        #         # Grab coursename
        #         coursename = courses[index]

        #         # add to chunk
        #         chunk += f"• {coursename}\n"

        #         # prime for next loop
        #         index += 1
                
        #     else:
        #         embed.add_field( name="hiii", value=chunk)
        #         embedlen += len(chunk)
        #         chunk = ""
            
        #     embed.add_field( name="hiiix2", value=chunk)

        desc += f'''\n**Suggested Commands**
                    {PREFIX}lookup <XXX000> <SEASON> <YEAR>
                    {PREFIX}grades <XXX000> <SEASON> <YEAR>'''
        
        embed.description = desc

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