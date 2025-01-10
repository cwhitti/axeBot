# strings
name="TestAxeBot"
prefix="test."

# define some common ids
claire=343857226982883339
owner=claire

#json file - for discord embed formatting
json_file = "json/embeds.json"

# path to the database
db_path = "database/NAUCourses.db"
PIE_CHART_FILE = "images/grades.jpg"

# colors
dft_color     = 0x6495ED # hex
success_color = 0x21D375 # hex
error_color   = 0xF95C52 # hex

# lists
admin_list=[owner]
staff_list=admin_list + []

# how often the bot updates (in hours)
HOURS_UPDATE = 12


# def calculate_term( szn, year ):

#     szn = szn.lower()

#     szn_dict = {
#                 "spring":"1",
#                 "summer":"4",
#                 "fall":"7",
#                 "winter":"8"
#                 }

#     return "1" + year[2:] + szn_dict[szn]

# OWNER=343857226982883339
# DFT_COLOR = 0x4287f5
# ERR_COLOR = 0xb52f43
# REACTION1 = "👀"
# REACTION2 = "👍"

# DFT_SZN = "spring"
# DFT_YEAR = "2025"
# DFT_TERM = calculate_term( DFT_SZN, DFT_YEAR )

# LOG_FILE = "logs/logs.txt"
# PIE_CHART_FILE = "grades.jpg"

# WAIT_LIMIT = 5
# GITLINK = "https://github.com/cwhitti/axeBot"
# CLIENT_ID = "1137314880697937940"
# CLIENT_PERMISSIONS = "117824"
# CLIENT_SCOPE =  "bot"
# MAX_TRIES = 9
