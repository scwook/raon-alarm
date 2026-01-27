import time
import datetime

from pathlib import Path

CLUE_ENABLE = True
BASE_DIR = Path(__file__).resolve().parent

def printConsole(message):
    if CLUE_ENABLE:
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + message)

def writeErrorLog(message, error=''):
    with open(BASE_DIR / 'error.log', 'a', encoding='utf-8') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            message = now + ' ' + message + '\n'
            file.write(message)

        if len(error):
            error = now + ' ' + str(error) + '\n'
            file.write(error)

def writeMessageLog(message):
    with open(BASE_DIR / 'coma.log', 'a', encoding='utf-8') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            message = now + ' ' + message + '\n'
            file.write(message)
