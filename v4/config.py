def calculate_term( szn, year ):

    szn = szn.lower()

    szn_dict = {
                "spring":"1",
                "summer":"4",
                "fall":"7",
                "winter":"8"
                }

    return "1" + year[2:] + szn_dict[szn]

OWNER=343857226982883339
DFT_COLOR = 0x4287f5
ERR_COLOR = 0xb52f43
REACTION1 = "👀"
REACTION2 = "👍"

DFT_SZN = "fall"
DFT_YEAR = "2024"
DFT_TERM = calculate_term( DFT_SZN, DFT_YEAR )

LOG_FILE = "logs/logs.txt"
PIE_CHART_FILE = "grades.jpg"

WAIT_LIMIT = 5
GITLINK = "https://github.com/cwhitti/axeBot"
CLIENT_ID = "1137314880697937940"
CLIENT_PERMISSIONS = "117824"
CLIENT_SCOPE =  "bot"
MAX_TRIES = 10