from flask import Flask, request, jsonify
import requests
import base64
from datetime import datetime

app = Flask(__name__)

access_token = ""

@app.route("/") 
def generate_access_token():
    global access_token
    
    consumer_key = "qCjC31ZoVf70EV1Y2MM6u7fl6u6A78YChgSfpQ5GYKBMAdNA"
    consumer_secret = "UeE52EtAVBM0p424K7lVbMqGMBgA9O1cqiQQrAgVjv61tFIxDeekAPDUvvDMngll"
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(access_token_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Failed to get access token'})

@app.route("/payment", methods=["GET"])
def make_payment():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bl12gZVWRTVGU4aF1530GO3mv3TM'
    }
    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNDI0MDkwNzAx",
        "Timestamp": "20240424090701",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254708374149",  # Ensure it's a string
        "PartyB": 174379,
        "PhoneNumber": "254113136019",  # Ensure it's a string
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of Bitches" 
    }

    stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    response = requests.post(stk_push_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return jsonify({'message': 'Payment was successful'})
    else:
        return jsonify({'error': 'Payment failed'}), 401

if __name__ == "__main__":
    app.run(debug=True)
