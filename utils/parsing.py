import re
from thefuzz import process, fuzz

char_abv_lookup = {
    # Annie
    "AN":           "AN",
    "ANN":          "AN",
    "ANNIE":        "AN",

    # Big Band
    "BB":           "BB",
    "BIG":          "BB",
    "BAND":         "BB",
    "BIGBAND":      "BB",
    "BIG BAND":     "BB",

    # Black Dahlia
    "BD":           "BD",
    "BL":           "BD",
    "BLA":          "BD",
    "BLACK":        "BD",
    "DAHLIA":       "BD",
    "B.DAHLIA":     "BD",
    "BLACK DAHLIA": "BD",

    # Beowulf
    "BW":           "BW",
    "BE":           "BW",
    "BEO":          "BW",
    "WU":           "BW",
    "WUL":          "BW",
    "WULF":         "BW",
    "WO":           "BW",
    "WOL":          "BW",
    "WOLF":         "BW",
    "BEOWULF":      "BW",

    # Cerebella
    "CE":           "CE",
    "CER":          "CE",
    "CLOWN":        "CE",
    "BEL":          "CE",
    "BELLA":        "CE",
    "CEREBELLA":    "CE",
    "CERABELLA":    "CE",

    # Double
    "DB":           "DB",
    "DO":           "DB",
    "DOU":          "DB",
    "DU":           "DB",
    "DBL":          "DB",
    "DOUB":         "DB",
    "DUB":          "DB",
    "DOUBLE":       "DB",

    # Eliza
    "EL":           "EL",
    "ELI":          "EL",
    "LIZ":          "EL",
    "LIZA":         "EL",
    "ELIZA":        "EL",

    # Filia
    "FI":           "FI",
    "FL":           "FI",
    "FIL":          "FI",
    "FILIA":        "FI",

    # Fukua
    "FU":           "FU",
    "FK":           "FU",
    "FUK":          "FU",
    "FUKUA":        "FU",

    # Marie
    "MA":           "MA",
    "MAR":          "MA",
    "MARIE":        "MA",

    # Ms. Fortune
    "MF":           "MF",
    "MI":           "MF",
    "FO":           "MF",
    "FOR":          "MF",
    "CAT":          "MF",
    "FORT":         "MF",
    "M.FORT":       "MF",
    "MS.FORT":      "MF",
    "MS. FORT":     "MF",
    "FORTUNE":      "MF",
    "MS. FORTUNE":  "MF",
    "MS.FORTUNE":   "MF",
    "MS FORTUNE":   "MF",
    "MSFORTUNE":    "MF",
    "MISS FORTUNE": "MF",

    # None
    "N":            "N",
    "-":            "N",
    "NONE":         "N",

    # Peacock
    "PC":           "PC",
    "PE":           "PC",
    "PEA":          "PC",
    "COCK":         "PC",
    "PEACOCK":      "PC",

    # Parasoul
    "PS":           "PS",
    "PA":           "PS",
    "PAR":          "PS",
    "PARA":         "PS",
    "SOUL":         "PS",
    "PARASOL":      "PS",
    "PARASOUL":     "PS",

    # Painwheel
    "PW":           "PW",
    "PAI":          "PW",
    "PAIN":         "PW",
    "WHEEL":        "PW",
    "PAINWHEEL":    "PW",

    # Robo-Fortune
    "RF":           "RF",
    "RB":           "RF",
    "ROB":          "RF",
    "ROBO":         "RF",
    "R FORT":       "RF",
    "RFORT":        "RF",
    "R. FORT":      "RF",
    "R.FORT":       "RF",
    "R FORTUNE":    "RF",
    "RFORTUNE":     "RF",
    "R. FORTUNE":   "RF",
    "R.FORTUNE":    "RF",
    "ROBOFORTUNE":  "RF",
    "ROBO FORTUNE": "RF",
    "ROBO-FORTUNE": "RF",

    # Squigly
    "SQ":           "SQ",
    "SQU":          "SQ",
    "SQUIG":        "SQ",
    "SQIGLY":       "SQ",
    "SQUIGLY":      "SQ",
    "SQUIGGLY":     "SQ",

    # Umbrella
    "UM":           "UM",
    "UMB":          "UM",
    "UMBY":         "UM",
    "BRELLA":       "UM",
    "UMBRELLA":     "UM",

    # Valentine
    "VA":           "VA",
    "VAL":          "VA",
    "VALENTINE":    "VA"
}

# Parse out "Annie/Bella/Band" into ("AN", "CE", "BB")
def parse_team(team: str):
    ret_chars = ["N", "N", "N"]
    # remove enclosers and split on dividers
    detected_chars = re.split(r"\s*[\|,/]\s*", re.sub(r"[\(\)\<\>]", "", team))
    # match against dictionary of aliases
    for i in range(len(detected_chars)):
        ret_chars[i] = fuzzymatch(detected_chars[i].upper().strip())
    return ret_chars[0], ret_chars[1], ret_chars[2]

# Fuzzy match against the alias dictionary
def fuzzymatch(name):
    # Look for an exact match first
    if name in char_abv_lookup:
        print(f"{name} := {char_abv_lookup[name]}")
        return char_abv_lookup[name]
    else:  
        choice = process.extractOne(name, char_abv_lookup.keys(), scorer=fuzz.ratio)
        print(f"{name} -> {choice[0]} -> {char_abv_lookup[choice[0]]}")
        return char_abv_lookup[choice[0]]