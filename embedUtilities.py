import discord
from classes import name_list


def bad_lookup_embed( search, attempt ):

    embed = discord.Embed(title="Sorry",
        description=f"'{msg}' is not a valid search.", color=search.color)

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

    embed = discord.Embed(title="Axe Bot Help",
        description="List of available commands:", color=axeBot.color)

    for command in axeBot.cmd_dict.keys():

        desc = axeBot.cmd_dict[command][1]

        embed.add_field(name=command, value=desc,inline=False)

    embed.set_footer(text="(!) This bot is not affiliated, sponsored, nor endorsed by NAU.")

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
        items_per_embed = 24 # discord embed limit

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

    return embed

def one_embed_course(axeBot, course):

    course_name = course.name
    course_description = course.desc
    course_units = course.units
    course_designation = course.desig
    course_semesters = course.semesters
    course_id = course.id
    course_url = course.url

    embed = discord.Embed(title=course_name, description="", color=axeBot.color)

    embed.add_field(name="Course ID:",
        value=course_id,
        inline=False)
    embed.add_field(name="Course Description:",
        value=course_description,
        inline=False)
    embed.add_field(name="Course Units:",
        value=course_units,
        inline=False)
    embed.add_field(name="Course Semesters:",
        value=course_semesters,
        inline=False)
    embed.add_field(name="Course Designation:",
        value=course_designation,
        inline=False)
    embed.add_field(name="",
        value=f"[Course Link]({course_url})",
        inline=False)

    return embed

def embed_working( axeBot ):

    embed = discord.Embed(title="Working on it...", description="", color=axeBot.color)

    embed.set_footer(text="This process may take up to one minute.")

    return embed

def github_embed( axeBot ):

    embed = discord.Embed(title="GitHub Link",
                        description=f"[Click here for the GitHub Link!]({axeBot.gitLink})",
                        color=axeBot.color)

    embed.set_footer(text="Thank you for enjoying axeBot :)")

    return [embed]
