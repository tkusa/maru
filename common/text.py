from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import random
import re
import string
from urllib.parse import urlparse
from common import config


# - find
# find pattern by regex
# reg: (string) regex pattern
# text: (string) search src
# return: (string) matched text
def find(reg, text):
    r = re.compile(reg)
    m = r.match(text)
    if m:
        return m.group()

    return ""


# - findAll
# find all patterns by regex
# reg: (string) regex pattern
# text: (string) search src
# return: (list) matched texts
def findAll(reg, text):
    r = re.compile(reg)
    matches = re.findall(reg, text)

    result = []
    for match in matches:
        if match == '':
            continue
        if match in result:
            continue
        result.append(match)

    return result


# - findTag
# find tag from html text
# tag: (string) tag name
# text: (string) search src
# return: (string) text wrapped in tag
def findTag(tag, text):
    soup = bs(text, features='html.parser')
    result = soup.find(tag)
    if not result:
        return ""

    return result.get_text()


# - replace
# find and replace pattern by regex
# reg: (string) regex pattern
# to: (string) replace to 
# text: (string) search src
# return: (string) replaced text
def replace(reg, to, text):
    r = re.compile(reg)
    result = r.sub(to, text)

    return result


# - randomAscii
# get a random ascii text
# len: (int) length of text
# return: (string) random text
def randomAscii(len=8):
    result = ''.join(
        random.choices(
            string.ascii_letters + string.digits, k=len
        )
    )
    return result


# - timestamp
# get a timestamp
# return: (string) timestamp
def timestamp():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    return timestamp


# - dirname
# get a dirname from path
# path: (string) path to check
# return: (string) timestamp
def dirname(path):
    dirname = os.path.dirname(path)
    return dirname


# - getExtension
# get a extension from resource url
# url: (string) resource
# return: (string) extension
def getExtension(url):
    # search from extension dict
    for ext, reg in config.EXTENSIONS.items():
        if re.search(reg, url):
            return "." + ext
    return ""

def getDomain(url: str):
    parsed = urlparse(url)
    return parsed.netloc

def getOrigin(url: str):
    url = stripUrl(url)
    reg = config.REGEX_ORIGIN
    match = re.search(reg, url)
    if match is None:
        return None
    return match.group()

def getPath(url: str):
    url = stripUrl(url)
    origin = getOrigin(url)
    if origin is not None:
        url = url.replace(origin, "", 1)
    reg = config.REGEX_PATH
    match = re.search(reg, url)
    if match is None:
        return None
    return match.group()    

def getParams(url: str):
    result = {}
    splitted = url.split("?")
    if len(splitted) >= 2:
        params = splitted[1]
        params = params.split("&")
        for param in params:
            vals = param.split("=")
            result[vals[0]] = vals[1]
    return result

def stripUrl(url: str):
    no_params = url.split("?")[0]
    result = no_params.split("#")[0]
    if result[-1] != "/":
        result = result + "/"
    return result





