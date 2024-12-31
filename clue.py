import time
import datetime

CLUE_ENABLE = True

def printConsole(pvName, message):
    if CLUE_ENABLE:
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + pvName + ' ' + message)

def writeErrorLog(message, error=''):
    with open('error.log', 'a', encoding='utf-8') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            message = '\n' + now + ' ' + message
            file.write(message)

        if len(error):
            error = '\n' + now + ' ' + str(error)
            file.write(error)