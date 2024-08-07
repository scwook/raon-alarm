import os
import time
import pymysql
import json

from flask import Flask, jsonify
from flask import request
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERVER_ADDR = 'localhost'
UPLOAD_FOLDER = '/data/asset_image'
DB_HOST = 'localhost'
DB_USER = 'scwook'
DB_PASSWORD = 'qwer1234'
DB_DATABASE = 'inventory'

@app.route('/inventory/insert', methods=['POST'])
def set_asset_list():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    inventory = conn.cursor()
    retrieve = conn.cursor()
    # jsonData = request.get_json()
    formData = request.form

    assetNumber = "'" + formData['assetNumber'] + "'"
    date = "'" + formData['assetDate'] + "'"
    deviceName = "'" + formData['assetName'] + "'"
    manager = "'" + formData['assetManager'] + "'"
    location = "'" + formData['assetLocation'] + "'"

    file = request.files['file']
    #sercureFileName = secure_filename(file.filename)
    fileName = "'" + file.filename + "'"
   
    retrieveQuery = 'SELECT * FROM asset_list WHERE AssetNumber LIKE ' + assetNumber
    retrieve.execute(retrieveQuery)
    result = retrieve.fetchall()

    if len(result):
        return 'overlap'

    insertQuery = 'INSERT INTO asset_list(AssetNumber,Date,DeviceName,Manager,Location,FileName) VALUES(' + assetNumber + "," + date + "," + deviceName + "," + manager + "," + location + "," + fileName + ")"

    inventory.execute(insertQuery)
    conn.commit()

    retrieveQuery = 'SELECT max(ID) FROM asset_list'
    inventory.execute(retrieveQuery)
    lastID = inventory.fetchone()[0]

    conn.close()

    folder = UPLOAD_FOLDER + '/' + str(lastID)
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    if file:
        file.save(os.path.join(folder, file.filename))
        return 'success'

    else:
        return 'fail'

   # return 'OK'
  #return json.dumps(jsonData)

@app.route('/inventory/update', methods=['POST'])
def update_asset_list():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    inventory = conn.cursor()
    retrieve = conn.cursor()

    formData = request.form

    referenceNum = "'" + formData['reference'] + "'"
    assetNumber = "'" + formData['assetNumber'] + "'"
    date = "'" + formData['assetDate'] + "'"
    deviceName = "'" + formData['assetName'] + "'"
    manager = "'" + formData['assetManager'] + "'"
    location = "'" + formData['assetLocation'] + "'"

    file = request.files['file']
    fileName = "'" + file.filename + "'"

    retrieveQuery = 'SELECT * FROM asset_list WHERE AssetNumber LIKE ' + assetNumber
    retrieve.execute(retrieveQuery)
    result = retrieve.fetchall()

    for x in retrieve:
        if x[1] != assetNumber:
            return 'overlap'

    updateQuery = 'UPDATE asset_list SET AssetNumber=' + assetNumber + ',Date=' + date + ',DeviceName=' + deviceName + ',Manager=' + manager + ',Location=' + location + ",FileName=" + fileName + ' WHERE AssetNumber=' + referenceNum

    inventory.execute(updateQuery)
    conn.commit()
    
    retrieveQuery = 'SELECT ID FROM asset_list WHERE AssetNumber=' + assetNumber
    inventory.execute(retrieveQuery)
    ID = inventory.fetchone()[0]

    conn.close()

    folder = UPLOAD_FOLDER + '/' + str(ID)
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    if file:
        file.save(os.path.join(folder, file.filename))
        return 'success'

    else:
        return 'fail'

@app.route('/inventory/retrieve/<asset>')
def get_asset_list(asset):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    inventory = conn.cursor()
    assetListArray = []

    search = asset.replace("*", "%")
    retrieveQuery = 'SELECT * FROM asset_list WHERE AssetNumber LIKE ' + "'" + search + "'"

    inventory.execute(retrieveQuery)

    for x in inventory:
        inventoryDic = {'id':x[0], 'assetNumber':x[1], 'date':x[2], 'deviceName':x[3], 'manager':x[4], 'location':x[5], 'fileName':x[6]}
        assetListArray.append(inventoryDic)
    
    conn.close()

    return json.dumps(assetListArray, ensure_ascii=False)

if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="9010")
