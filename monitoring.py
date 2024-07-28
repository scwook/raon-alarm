import time
import pymysql
import json

from pvaccess import *
from flask import Flask, jsonify
from flask_cors import CORS

SERVER_ADDR = "192.168.68.126"

pvObjectDict = dict()

class ChannelMonitor:
    def __init__(self, name):
        self.name = name

    def monitor(self, data):
        pvObjectDict[self.name] = dict(data)
        
        if type(pvObjectDict[self.name]['value']) is dict:
            pvObjectDict[self.name]['value'] = pvObjectDict[self.name]['value']['index']

### Read Channel List
pvList = list(line.strip() for line in open('pvList'))

channelList = list()
monitoringList = list()

index = 0
for name in pvList:
        channelList.append(Channel(name, ProviderType.CA))
        monitoringList.append(ChannelMonitor(name))

        channelList[index].monitor(monitoringList[index].monitor, 'field(value,alarm)')
        index += 1

### Flask App
app = Flask(__name__)
CORS(app)

@app.route('/epics/retrieve')
def get_data():
        return json.dumps(pvObjectDict)


if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="9012")
