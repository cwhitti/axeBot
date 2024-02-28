import discord
from classes import name_list


def bad_lookup_embed( axeBot, msg ):

    embed = discord.Embed(title="Sorry",
        description=f"'{msg}' is not a valid search.", color=axeBot.color)

    embed.set_footer( text=f"(!) Commands can be found with {axeBot.prefix}help")

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
            f"- {pfx}lookup CS249\n",
            f"- {pfx}lookup BIO 181L Spring 2011    \n",
            f"- {pfx}lookup ANT winter 2022        \n",
            f"- {pfx}lookup cs212 summer 2017      \n",
            f"- {pfx}lookup eng      \n",
            f"- {pfx}subjects                    \n",
            f"- {pfx}invite                    \n\n",
            f"(!) This bot is not affiliated, sponsored, nor endorsed by NAU (!) \n\n",
            "==============   All Commands  =============="
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

    embed.set_footer(text=f"Based on {szn} {course_cat} catalogue")

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

def embed_grades( search, grades ):

    embed = discord.Embed(title="Invite me!",
                        description=f"Click [here]({url}) to invite axeBot to your server!",
                        color=axeBot.color)
    
