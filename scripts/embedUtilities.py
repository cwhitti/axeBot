from .subjectAbrvs import name_list
import discord

def bad_grade_lookup( axeBot, search ):

    embed = discord.Embed(title=f" Sorry, we couldn't find that course.",
        description=f"", color=axeBot.color)

    embed.add_field(name="",
                    value=f'''
                            **Common Failure Reasons**

                            👉   **No Records**: Public records not yet available, or class does not exist.

                            👉   **Incorrect Format**: The format for this command is *{axeBot.prefix}grades <SEASON> <YEAR>*.

                            ''')
    return [embed]

def bad_lookup_embed( axeBot, msg ):

    embed = discord.Embed(title="Sorry",
        description=f"'{msg}' is not a valid search.", color=axeBot.color)

    embed.set_footer( text=f"(!) Commands can be found with {axeBot.prefix}help")

    return [embed]

def class_not_offered( search ):

    szn = search.search_szn.capitalize()
    yr = search.search_year

    code = search.search_code

    new_szn = szn
    new_year = yr

    if szn == "Fall":
        new_szn = "Summer"

    elif szn == "Summer":
        new_szn = "Spring"

    elif szn == "Spring":
        new_szn = "Winter"
        new_year = int(yr) - 1

    else:
        new_szn = "Fall"

    embed = discord.Embed(title=f"{code}: No Records Found ",
        description="", color=search.color)

    embed.add_field(name="", value= f'''

        **Term**
        {szn} {yr}

        **What happened?**
        This class may not exist in the system due to one of the following reasons:

        👉   **Too Few Students**: To protect student privacy, grade distributions are not available for undergraduate classes with fewer than ten students enrolled or for graduate classes with fewer than five students enrolled.

        👉   **No Records**: Public records not yet available.

        👉   **Off-season**: Some classes are Spring/Fall only. Try searching for another semester.

        **Suggested commands:**
        axe.help
        axe.grades {code} {new_szn} {new_year}
        ''',
        inline=False)

    return [embed]

def create_subjects_embed(axeBot, name_list):

    embed = discord.Embed(title="NAU Subjects",
        description="List of available topics:",
        color=axeBot.color)

    start_letter = 'A'
    name_string = ""

    for name in name_list:

        if name_string != "":

            if name[0] == start_letter:
                name_string += f", {name}"

            else:
                embed.add_field(name="", value=name_string, inline=False)
                start_letter = name[0]
                name_string = ""
        else:
            name_string = f"{name}"

    embed.add_field(name="", value=name_string, inline=False)

    return embed

def create_help_embed(axeBot):

    pfx = axeBot.prefix

    desc = ("This bot was created to search up classes from the comfort",
            " of Discord. Because looking for classes can be annoying,",
            " the creators of this bot wanted a novel way to search them up.",
            "\n\n",

            "Usage examples:\n",
            "\n**Lookup**\n",
            f"- {pfx}lookup CS249\n",
            f"- {pfx}lookup BIO 181L Spring 2011    \n",
            f"- {pfx}lookup cs212 summer 2017      \n",
            f"- {pfx}lookup eng      \n",
            "\n**Grades**\n",
            f"- {pfx}grades CS126L      \n",
            f"- {pfx}grades mat136 summer 2022        \n",
            "\n**Subjects**\n",
            f"- {pfx}subjects                    \n",
            "\n**Invite**\n",
            f"- {pfx}invite                    \n\n",
            f"(!) This bot is not affiliated, sponsored, nor endorsed by NAU (!) \n\n",
            "**+===+ All Commands +===+**"
        )

    embed = discord.Embed(title="Hello from axeBot!",
                            description=''.join(desc), color=axeBot.color)

    for command in axeBot.cmd_dict.keys():

        desc = axeBot.cmd_dict[command][1]

        embed.add_field(name=command, value=desc,inline=False)
    embed.set_thumbnail(url="https://i.pinimg.com/564x/4a/25/80/4a25805f04f4ba694d9fff4a41426799.jpg")
    embed.set_footer(text="Created by Claire Whittington (Data Science '25)")

    return embed

def embed_courses( axeBot ):

    course_list = axeBot.course_list
    embed_list = []

    # Embed the full class
    if len(course_list) <= 5:

        for course in course_list:

            #embed course
            embed = one_embed_course( axeBot, course)
            embed_list.append( embed )

    # shows a list of names to look up
    elif len(course_list) > 5:

        total_items = len(course_list)
        items_per_embed = 25 # discord embed limit

        first = True

        for index in range(0, total_items, items_per_embed):

            batch_keys = course_list[index:index + items_per_embed]

            embed = batch_embed_course(axeBot, batch_keys, first)
            embed_list.append ( embed )

            first = False

    return embed_list

def batch_embed_course(axeBot, course_list, first_embed):

    # show title
    if first_embed == True:
        embed = discord.Embed(title=f"{len(axeBot.course_list)} RESULTS FOUND",
                                color=axeBot.color)

    # no title
    else:
        embed = discord.Embed(title="", color=axeBot.color)

    # add names
    for course in course_list:

            embed.add_field(name=course.name, value=f"CourseID: {course.id}",
                            inline=False)

    embed.set_footer(text=f"Courses listed may not be currently available.")
    return embed

def one_embed_course(search, course):

    course_name = course.name
    course_description = course.desc
    course_units = course.units
    course_designation = course.desig
    course_semesters = course.offered
    course_id = course.id
    course_url = course.url
    course_prereqs = course.prereqs
    course_cat = search.search_year
    szn = search.search_szn

    embed = discord.Embed(title=course_name, description="", color=search.color)

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

    return embed

def embed_working( axeBot ):

    embed = discord.Embed(title="Working on it...", description="", color=axeBot.color)

    embed.set_footer(text="This process may take up to one minute.")

    return embed

def github_embed( axeBot ):

    embed = discord.Embed(title="GitHub Link",
                        description=f"Click [here]({axeBot.gitLink}) for the GitHub Link!",
                        color=axeBot.color)

    embed.set_footer(text="Thank you for enjoying axeBot :)")

    return [embed]

def invite_embed( axeBot, url ):

    embed = discord.Embed(title="Invite me!",
                        description=f"Click [here]({url}) to invite axeBot to your server!",
                        color=axeBot.color)

    embed.set_footer(text="Thank you for enjoying axeBot :)")

    return embed

def create_grade_embed( search, course ):

    CHAR = '.'
    WIDTH = 98

    name = course.name
    szn = search.search_szn.capitalize()
    year = search.search_year
    section = course.section
    prof = course.prof
    A = int(course.A)
    B = int(course.B)
    C = int(course.C)
    D = int(course.D)
    F = int(course.F)
    AU = int(course.AU)
    P = int(course.P)
    NG = int(course.NG)
    W = int(course.W)
    I = int(course.I)
    IP = int(course.IP)
    pen = int(course.pen)
    total = int(course.total)

    embed = discord.Embed(title=f"{name} Section {section} Grade Distribution",
                        description="",
                        color=search.color)
    #embed.add_field(name=f"{DESIGN1 * X_CHR} Class Info {DESIGN1 * X_CHR}", value="", inline=False)
    #embed_section_title(embed, WIDTH, CHAR, "Class Info")
    embed.add_field(name="Professor", value=course.prof, inline=True)
    embed.add_field(name="Term", value=f"{szn} {year}", inline=False)
    embed.add_field(name="Section", value=course.section, inline=False)

    dropped = ( W / total ) * 100

    # Check if pass/fail
    if ( A + B + C + D == 0 ):

        passed = (P / total) * 100
        failed = (100 - passed - dropped)

    # graded class
    else:

        passed_sum = A + B + C
        passed = (passed_sum / total) * 100
        failed = (100 - passed - dropped)

    embed.add_field(name="",
                value="",
                inline=False)
    embed.add_field(name="Passed",
                    value="✅ "  + str( round( passed, 2 ) ) + "%",
                    inline=True)
    embed.add_field(name="",
                    value="_\* Passing grades are counted as A, B, C_",
                    inline=True)
    embed.add_field(name="Dropped",
                    value="⚠️ "  + str( round( dropped, 2 ) ) + "%",
                    inline=False)
    embed.add_field(name="Failed ",
                    value="🛑 "  + str( round( failed, 2 ) ) + "%",
                    inline=False)
    #embed_section_title(embed, WIDTH, CHAR, "Class Grades")

    text = ""

    embed.add_field(name=f"",
                    value=f'''
                    **{course.total} Total Enrolled**

                    ''',
                    inline=False)

    if ( A + B + C + D != 0 ):


        add_grade(embed, text + "A", course.A)
        add_grade(embed, text + "B", course.B)
        add_grade(embed, text + "C", course.C)
        add_grade(embed, text + "D", course.D)
        add_grade(embed, text + "F", course.F)
        add_grade(embed, text + "W", course.W)

    else:

        add_grade(embed, text + "P", course.P)
        add_grade(embed, text + "F", course.F)
        add_grade(embed, text + "W", course.W)

    #embed_last_line( embed, WIDTH, CHAR )


    #embed.add_field(name = "", value ='''
    #    (!) To protect student privacy, grade distributions are not
    #    available for undergraduate classes with fewer than ten
    #    students enrolled or for graduate classes with fewer
    #    than five students enrolled.
    #
    #    (!) Only class after 2005 have public records available''' , inline=False)

    #embed_last_line( embed, WIDTH, '=' )

    embed.set_footer(text=f"Based on {szn} {year} records.")
    embed.set_thumbnail(url="https://i.pinimg.com/564x/4a/25/80/4a25805f04f4ba694d9fff4a41426799.jpg")

    return embed

def embed_new_line( embed ):

    embed.add_field(name="\u200B", value="\u200B", inline=False) # Empty line

def add_grade(embed, text, grade):

    str = f"{text}: {grade}"

    embed.add_field(name=str, value="")

def embed_section_title(embed, width, CHAR, text):

    """
    Center the given text inside a design.

    Args:
    - text (str): The text to be centered.
    - width (int): The width of the design.

    Returns:
    - str: The centered text inside the design.
    """

    if len(text) >= width:
        return text

    padding = (width - len(text)) // 2
    left_padding = padding
    right_padding = width - len(text) - left_padding
    centered_text = CHAR * left_padding + f" {text} " + CHAR * right_padding

    embed.add_field(name=centered_text, value="", inline=False)

def embed_last_line( embed, width, CHAR ):

    embed.add_field(name=CHAR * (int(width/2) + 8), value="", inline=False)
