import time
import datetime

CLUE_ENABLE = True

def printConsole(message):
    if CLUE_ENABLE:
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + message)

def writeErrorLog(message, error=''):
    with open('error.log', 'a', encoding='utf-8') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            message = now + ' ' + message + '\n'
            file.write(message)

        if len(error):
            error = now + ' ' + str(error) + '\n'
            file.write(error)

def writeMessageLog(message):
    with open('message.log', 'a', encoding='utf-8') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            message = now + ' ' + message + '\n'
            file.write(message)