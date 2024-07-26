import discord 
import config as cfg
import scripts.pieChart as pc
from datetime import datetime
from classes.CourseClass import Course


class myEmbed:
    '''
    PUBLIC FUNCTIONS
    '''

    def embed_grades( self, embed, search, courses:list ):
        
        filename = cfg.PIE_CHART_FILE
        pc.create_figure( filename, courses)

        embed.set_footer(text=f"Based on {search.szn} {search.year} records.")
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