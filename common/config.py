from protocols.http.method import HttpMethod

# Control
LF = "\n"
SLASH = "/"

# Colors
COLOR_RED = "\x1b[31;20m"
COLOR_GREEN = "\x1b[32;20m"
COLOR_YELLOW = "\x1b[33;20m"
COLOR_RESET = "\x1b[0m"

# Path to dirs
DIR_LOG = "./dev/logs"
DIR_TMP = "./dev/tmp"
DIR_SAVE = "./dev/storage"
DIR_WORDLIST = "./dev/wordlist"

# Regex
REGEX_URL = 'http[s]*://[^"]*'
REGEX_ORIGIN = '^(http[s]?:)?//[^?#/]+'
REGEX_PATH = '^[/|./|../]?.*$'
REGEX_RESOURCE = '(?=.*\.jpg|.*\.jpeg|.*\.png|.*\.mp4)http[s]*://[^"]*'

# Extension dict
EXTENSIONS = {
    "jpg": "(?=.*\.jpg|.*\.jpeg).*",
    "png": "(?=.*\.png).*",
    "mp4": "(?=.*\.mp4).*",
}

# HTTP config
HTTP_HEADERS = {
    "User-Agent": "maru"
}

HTTP_METHODS = [
    HttpMethod.GET, 
    HttpMethod.POST, 
    HttpMethod.PUT, 
    HttpMethod.DELETE, 
    HttpMethod.PATCH
]
HTTP_BLACKLIST = [404]

# Max threads
MAX_THREADS = 3
