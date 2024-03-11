import datetime
from common import config, io


# - log
# log a message
# message: (string) message to log
def log(message):
    # get timestamp
    now = datetime.datetime.now()
    # log file rotate everyday
    file_path = config.DIR_LOG + "/" + str(now.date()) + ".log"

    # write to log file
    timestamp = "[" + str(now)+ "] "
    content = timestamp + message + config.LF
    io.append(file_path, content)


# - success
# output a message with success format
# message: (string) message to output
def success(message):
    format = "[+] " + config.COLOR_GREEN + message + config.COLOR_RESET
    print(format)
    log(message)


# - fail
# output a message with fail format
# message: (string) message to output
def fail(message):
    format = "[-] " + config.COLOR_RED + message + config.COLOR_RESET
    print(format)
    log(message)


# - warn
# output a message with warn format
# message: (string) message to output
def warn(message):
    format = "[!] " + config.COLOR_YELLOW + message + config.COLOR_RESET
    print(format)
    log(message)


# - info
# output a message with info format
# message: (string) message to output
def info(message):
    format = "[?] " + message
    print(format)
    log(message)