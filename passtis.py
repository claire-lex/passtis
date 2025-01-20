# Passtis
# Very stupid password dictionary builder for french dictionaries
#
# Lex @ https://github.om/claire-lex/passtis - 2021
#
# pylint: disable=invalid-name

"""
usage: passtis.py [-h] [-w words] [-f file] [-p postcode (69|69100)]
[-s specialchars] [-m] [-d] [-y] [-n] [-x]

French password dictionary builder

optional arguments:
  -h, --help            show this help message and exit
  -w word(s), --words word(s)
                        Comma-separated word(s) to use
  -f file, --file file  File containing a list of words
  -p postcode (69|69100), --postcode postcode (69|69100)
                        Postcode to use (all other are moved)
  -s specialchars, --special specialchars
                        Special chars to use (can be empty string)
  -m, --month           Use months as base (in french)
  -d, --date            Use dates as suffix with format ddmmyy
  -y, --year            Use years as suffix with format yyyy
  -n, --noleet          Do not use leet transformations on words (e.g. P@ssw0rd$)
  -x, --nocombo         Do not build combined words with short words
"""

from os.path import join, dirname
from datetime import date, timedelta
from argparse import ArgumentParser
from itertools import combinations, product

#-----------------------------------------------------------------------------#
# Constants & config                                                          #
#-----------------------------------------------------------------------------#

# Values that may change -----------------------------------------------------#

MIN_YEAR = 2000
MAX_YEAR = 2022
SPECIALS = "&#@+$%*?/!§"
COMBO_MAX_LEN = 5 # Maximum length of words that will be combined
WORDS = [] # Can be changed with options 'words' and 'file'

# Arguments parsing ----------------------------------------------------------#

OPTS_DICT = (
    ("-w", "--words", "Comma-separated word(s) to use", WORDS, "word(s)"),
    ("-f", "--file", "File containing a list of words", None, "file"),
    ("-p", "--postcode", "Postcode to use (all other are moved)", None, "postcode (69|69100)"),
    ("-s", "--special", "Special chars to use (can be empty string)", None, "specialchars"),
    ("-l", "--minlength", "Minimum length", None, "length"),
    ("-m", "--month", "Use months as base (in french)", False, None),
    ("-d", "--date", "Use dates as suffix with format ddmmyy", False, None),
    ("-y", "--year", "Use years as suffix with format yyyy", False, None),
    ("-n", "--noleet", "Do not use leet transformations on words (e.g. P@ssw0rd$)", False, None),
    ("-x", "--nocombo", "Do not build combined words with short words", False, None)
)

def init_options() -> object:
    """Set options using ``ArgumentParser``."""
    args = ArgumentParser(description="French password dictionary builder")
    # Store all other options
    for opt in OPTS_DICT:
        if not opt[4]: # Option takes no argument (no meta)
            args.add_argument(opt[0], opt[1], help=opt[2],
                              action='store_true', default=opt[3])
        else:
            args.add_argument(opt[0], opt[1], help=opt[2],
                              metavar=opt[4], default=opt[3])
    return args.parse_args()

OPTIONS = init_options()

# Regular stuff --------------------------------------------------------------#

# 0-10 and 00-09
NUM = [str(x) for x in list(range(0, 100))]
NUM += [str(x).zfill(2) for x in list(range(0, 10))]
# Sequence (from 123 to 123456789 and from 0123 to 0123456789)
suite1 = [str(x) for x in range(1, 10)]
NUM += ["".join(suite1[:x]) for x in range(3,10)]
suite0 = [str(x) for x in range(0, 10)]
NUM += ["".join(suite0[:x]) for x in range(4,10)]
# Special sequence
NUM += ["456", "789"]

if OPTIONS.special != None: # Can be empty string
    SPECIALS = OPTIONS.special

# Leet mode ------------------------------------------------------------------#

# List taken from psudohash (https://github.com/t3l3machus/psudohash)
# Don't forget to check this awesome tool!
LEET_TABLE = {
    'a' : ['@', '4'],
    # 'b' : ['8'],
    'e' : ['3'],
    # 'g' : ['9', '6'],
    'i' : ['1', '!'],
    'o' : ['0'],
    's' : ['$', '5'],
    't' : ['7']
}

# Dates ----------------------------------------------------------------------#

MONTHS = []
if OPTIONS.month:
    MONTHS = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet",
              "aout", "septembre", "octobre", "novembre", "decembre"]

YEARS = []
if OPTIONS.year:
    YEARS = [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)]

DATES = []
if OPTIONS.date:
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    DATES = [x.strftime("%d%m%y") for x in daterange(date(MIN_YEAR, 1, 1), date(MAX_YEAR, 12, 31))]

# Post codes -----------------------------------------------------------------#

POSTCODES = []
if OPTIONS.postcode:
    # French post/zip code using INSEE's list
    POSTCODES_FILE = join(dirname(__file__), "postcode_insee_20210923.csv")
    with open(POSTCODES_FILE, 'r', encoding='ISO-8859-1') as fd:
        postcodes = [x.strip().split(";")[1] for x in fd]
    # We add department number (ex: 69 for 69***, 974)
    postcodes += [str(x).zfill(2) for x in list(range(1, 96))] + [str(x) for x in range(974, 989)]
    # Now we take only the ones we need
    selected = [OPTIONS.postcode] if "," not in OPTIONS.postcode else OPTIONS.postcode.split(",")
    POSTCODES += selected
    for pc in selected:
        POSTCODES += [x for x in postcodes if x.startswith(pc)]

# Words from arguments and files ---------------------------------------------#

# -w / --words
if OPTIONS.words:
    WORDS += [x.strip() for x in OPTIONS.words.split(",")]

# -f / --file
if OPTIONS.file:
    try:
        with open(OPTIONS.file, 'r', encoding='utf-8') as fd:
            WORDS += [x.strip() for x in fd]
    except IOError:
        print("Error: File {0} cannot be opened.".format(OPTIONS.file))
        exit(-1)
        
# Short user-supplied words (less than N chars) are used to build combined
# words, unless option -n / --nocombo is supplied.
# Example: words 'user' and 'ext' will combined into 'userext' and 'extuser'
if not OPTIONS.nocombo:
    short_words = [x for x in WORDS if len(x) < COMBO_MAX_LEN]
    combos = [x for x in combinations(short_words, 2)]
    WORDS += ["".join(x) for x in combos] # Regular: [user, ext] == userext
    WORDS += ["".join(y) for y in combos[::1]] # Reverse: extuser

def leet_transformations():
    results = []
    for word in WORDS:
        combinations = []
        for char in word:
            if char in LEET_TABLE:
                combinations.append(LEET_TABLE[char] + [char])
            else:
                combinations.append([char])
            # Générer toutes les combinaisons possibles
        results += [''.join(combination) for combination in product(*combinations)]
    return results

# We create leet transformations for each words, see LEET_TABLE for details
if not OPTIONS.noleet:
    WORDS += leet_transformations()
    
# Remove duplicates
WORDS = list(set(WORDS))

# Final format ---------------------------------------------------------------#

BASE = WORDS + MONTHS
SUFFIX = NUM + YEARS + POSTCODES + DATES
FORMATS = [
    (BASE, SUFFIX), # Thierry42
    (BASE, SPECIALS), # Bernard*
    # (SUFFIX, SPECIALS), # 260143! - Weird result but uncomment if you need it
    (BASE, SUFFIX, SPECIALS), # Bernard42!
    (BASE, SPECIALS, SUFFIX)  # Thierry@2021
]

try:
    MINLENGTH = int(OPTIONS.minlength) if OPTIONS.minlength else 0
except ValueError:
    print("Error: Invalid value for minimum length argument.")
    exit(-1)
    
#-----------------------------------------------------------------------------#
# Run                                                                         #
#-----------------------------------------------------------------------------#

def psprint(entry):
    if len(entry) >= MINLENGTH:
        print(entry)

# Base only
for base in BASE:
    psprint(base)

# Iterate over formats (very dirty code, I expect to be more inspired later)
for pformat in FORMATS:
    for item1 in pformat[0]:
        for item2 in pformat[1]:
            if len(pformat) == 2:
                psprint("".join([item1, item2]))
                psprint("".join([item1, item2]).capitalize())
            elif len(pformat) == 3:
                for item3 in pformat[2]:
                    psprint("".join([item1, item2, item3]))
                    psprint("".join([item1, item2, item3]).capitalize())
