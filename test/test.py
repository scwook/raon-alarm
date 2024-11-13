from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

SERVER_ADDR = '192.168.131.161'

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def test():
    return "OK"

if __name__ == "__main__":
    
    app.run(host=SERVER_ADDR, port="8000")