def embed_past_sections( searchInfo, records ):

    sections = 1
    last_term = ""
    desc = ''

    # initialize new list so we can store term data
    season, year = searchInfo.calculate_year_and_season( searchInfo.term )

    desc = f'''Public grades for {searchInfo.search_code} have been found. Please refer to the following:

    '''

    # loop through records
    for record in reversed(records):

        # get the term
        term = record.term

        if term == last_term:
            sections += 1
        
        else:

            if last_term != "":
                season, year = searchInfo.calculate_year_and_season( term )
                desc  += f"‣ {season} {year} - {sections} sections\n"

            last_term = term
            sections = 1
    return desc
    
def embed_grades( records ):
        
    desc = ""

    for record in records:
        details = embed_course_grades( record )

        if len(details) + len(desc ) <= 4000:

            desc += details
        
        else:
            desc += "```Omitted 1 Class```"


    if len( desc) > 4096:
        desc = "```ERROR: Too many classes to display!```"

    return desc


# def embed_course( self, embed, course, search ):

#     course_name = course.title
#     course_description = course.desc
#     course_units = course.units
#     course_designation = course.desig
#     course_semesters = course.offered
#     course_id = course.courseID
#     course_url = course.url2
#     course_prereqs = course.prereqs
#     course_cat = search.year
#     szn = search.szn

#     embed.title = course_name

#     embed.add_field(name="Course ID:",
#         value=course_id,
#         inline=False)
#     embed.add_field(name="Description:",
#         value=course_description,
#         inline=False)
#     embed.add_field(name="Units:",
#         value=course_units,
#         inline=False)
#     embed.add_field(name="Current Offerings:",
#         value=course_semesters,
#         inline=False)
#     embed.add_field(name="Prerequisites:",
#         value=course_prereqs,
#         inline=False)
#     embed.add_field(name="Requirement Designation:",
#         value=course_designation,
#         inline=False)
#     embed.add_field(name="",
#         value=f"[Course Link]({course_url})",
#         inline=False)

#     embed.set_footer(text=f"Based on {szn.capitalize()} {course_cat} catalogue")

def embed_course_grades( course ):

    # initialzie variables
    details = f''''''
    a = int(course.A)
    b = int(course.B)
    c = int(course.C)
    d = int(course.D)
    f = int(course.F)
    w = int(course.W)
    p = int(course.P)
    total = int(course.Total)

    # see if the course was pass/fail course
    if a + b + c + d == 0:
        
        # calculate percentages of passed and failed
        pct_pass = round((p / total) * 100, 2)
        pct_fail = round((f / total) * 100, 2) 
        pct_w = round((w / total) * 100, 2)

    else:

        # calculate passed and failed totals
        passed = a + b + c
        failed = d + f
        
        # calculate percentages of passed and failed
        pct_pass = round((passed / total) * 100, 2)
        pct_fail = round((failed / total) * 100, 2) 
        pct_w = round((w / total) * 100, 2)


    details += \
    f'''
    **Section {course.section} - {course.instructor}**
        ```
✅ {pct_pass}% Passed
🚸 {pct_w}% Dropped
🛑 {pct_fail}% Failed
👥 {total} Enrolled ```
        '''

    return details 

def embed_subject( embed, courses:list ):

    desc = f"\n**Listing {len(courses)} courses:\n**"
    embed.description = desc

    chunk = ""

    # embed the courses, just the numbers
    for coursename in courses:

        #line = f"• {coursename}\n"
        words = coursename.split()
        line = f"• {words[0]}{words[1]}\n"
        desc += line
    
    embed.description = desc

def set_img( self, img_url, embed ):
    embed.set_image( url = img_url)
