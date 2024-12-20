import time
import datetime

CLUE_ENABLE = True

def printConsole(pvName, message):
    if CLUE_ENABLE:
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + pvName + ' ' + message)

def writeErrorLog(message, error):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = '\n' + now + ' ' + message
    error = '\n' + now + ' ' + str(error)

    with open('error.log', 'a', encoding='utf-8') as file:
        file.write(message)
        file.write(error)