from flask import Flask, request
app = Flask(__name__)
import os
from main import get_celo_price as celo_price


response = ""

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response  
    text = request.values.get("text", "default")

    if text == '':
        response = "CON Get the Price of Celo blockchain tokens \n"
        response += "1. Price of Celo \n"

    elif text == '1':
        response = "CON Choose account information you want to view \n"
        response = "The price of celo is: " + celo_price
    
    return response

if __name__ == '__main__':
    app.run (host="0.0.0.0", port=os.environ.get('PORT'), debug=False)