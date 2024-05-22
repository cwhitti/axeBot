def calculate_term( szn, year ):

    szn = szn.lower()

    szn_dict = {
                "spring":"1",
                "summer":"4",
                "fall":"7",
                "winter":"8"
                }

    return "1" + year[2:] + szn_dict[szn]

DEFAULT_SZN = "fall"
DEFAULT_YEAR = "2024"
DEFAULT_TERM = calculate_term( DEFAULT_SZN, DEFAULT_YEAR )
