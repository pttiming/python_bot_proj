from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
import api


app = Flask(__name__)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_num = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()
    info = {"Number": incoming_num, "Message": incoming_msg}
    responded = False
    if 'subscribe' in incoming_msg:
        print(info)
        r = requests.post('https://localhost:44325/api/message/', json=info, verify=False)
        hello = r.text
        msg.body(hello)
        responded = True
    if 'races' in incoming_msg:
        print(info)
        r = requests.post('https://localhost:44325/api/message/', json=info, verify=False)
        hello = r.text
        msg.body(hello)
        responded = True
    if not responded:
        msg.body('Welcome to the Virtual Info Tent.  Please let me know how I can help you. '
                 'For a list of Races I can help with, reply RACES')
    return str(resp)


@app.route('/send', methods=['POST', 'GET'])
def send():
    req_data = request.get_json()
    number = req_data['number']
    body = req_data['body']
    media_url = req_data['media_url']
    resp = MessagingResponse
    account_sid = api.account_sid
    auth_token = api.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=body,
            media_url=media_url,
            from_='+14144200792',
            to=number
        )

    print(message)
    return str(resp)
