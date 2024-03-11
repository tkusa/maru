import datetime
import os
import glob
from common import config, log, io, text


# - write
# write content to a file
# path: (string) path to a file
# content: (string, byte) content to write
# return: (bool) success/fail
def write(path, content):
    try:
        with open(path, "wb") as f:
            f.write(content)
            return True
    except FileNotFoundError as e:
        log.fail("File '" + path + "' not found: " + e.strerror)
        return False
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return False


# - append
# append content to a file
# path: (string) path to a file
# content: (string, byte) content to write
# return: (bool) success/fail
def append(path, content):
    try:
        with open(path, "a+") as f:
            f.write(content)
            return True
    except FileNotFoundError as e:
        log.fail("File '" + path + "' not found: " + e.strerror)
        return False
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return False


# - read
# read contents from a file
# path: (string) path to a file
# byte: (bool) read as byte/string
# return: (bool) success/fail
def read(path, byte=False):
    # option setting
    opt = "r"
    # read as bytes
    if byte:
        opt = "rb"
    try:
        with open(path, opt) as f:
            content = f.read()
            return content
    except FileNotFoundError as e:
        log.fail("File '" + path + "' not found: " + e.strerror)
        return ""
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return ""


# - writeLines
# write contents by line
# path: (string) path to a file
# contents: (list) contents to write
# return: (bool) success/fail
def writeLines(path, contents):
    for content in contents:
        # write a line
        line = content + config.LF
        result = append(path, line)
        if not result:
            break

    return result


# - readLines
# read contents by line
# path: (string) path to a file
# return: (list) contents by line
def readLines(path):
    # make a list from contents
    content = read(path)
    lines = content.split(config.LF)

    result = []
    for line in lines:
        # remove empty element
        if line == '':
            continue
        result.append(line)

    return result


# - remove
# remove a file
# path: (string) path to a file
# return: (bool) success/fail
def remove(path):
    try:
        os.remove(path)
        return True
    except FileNotFoundError as e:
        log.fail("File '" + path + "' not found: " + e.strerror)
        return False


# - mkdir
# make a dir
# path: (string) path to a dir
# return: (bool) success/fail
def mkdir(path):
    # dir already exists
    if os.path.exists(path):
        return True

    try:
        os.mkdir(path)
        return True
    except FileNotFoundError as e:
        log.fail("Dir '" + path + "' cannot create: " + e.strerror)
        return False
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return False


# - rmdir
# remove a dir
# path: (string) path to a dir
# return: (bool) success/fail
def rmdir(path):
    try:
        os.rmdir(path)
        return True
    except FileNotFoundError as e:
        log.fail("Dir '" + path + "' cannot delete: " + e.strerror)
        return False
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return False


# - randomDir
# make a tmp dir with random name
# return: (string) path to created dir
def randomDir():
    result = False
    mkdir(config.DIR_TMP)
    while not result:
        # make a dir in tmp with random name
        dirname = text.timestamp() + text.randomAscii()
        path = config.DIR_TMP + config.SLASH + dirname
        result = mkdir(path)

    return path
        
        
# - removeAll
# remove all files in dir
# dir: (string) path to a dir
# return: (bool) success/fail
def removeAll(dir):
    # all files in dir
    files = glob.glob(dir + config.SLASH + "*")
    result = True
    for file in files:
        r = remove(file)
        # failed to remove file
        if not r:
            result = False
    return result


# - concatAll
# concatenate all files in dir
# path: (string) path to save concatenated file
# dir: (string) path to a dir
# return: (bool) success/fail
def concatAll(path, dir):
    # all files in dir
    files = glob.glob(dir + config.SLASH + "*")
    # get filenames to sort
    filenames = [os.path.basename(file) for file in files]
    sorted_files = sorted(filenames, key=int)

    try:
        with open(path, "wb") as out:
            for f in sorted_files:
                # read file as byte
                content = read(dir + config.SLASH + f, byte=True)
                out.write(content)
        return True

    except FileNotFoundError as e:
        log.fail("Dir '" + dir + "' not found: " + e.strerror)
        return False
    except ValueError as e:
        log.fail("Path '" + path + "' is invalid.")
        return False



