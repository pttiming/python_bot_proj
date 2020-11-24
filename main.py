from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json


app = Flask(__name__)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_num = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()
    info = {"Number": incoming_num}
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'dog' in incoming_msg:
        dog = requests.get('https://dog.ceo/api/breeds/image/random')
        if dog.status_code == 200:
            data = dog.json()
            link = f'{data["message"]}'
        msg.media(link)
        responded = True
    if 'movie' in incoming_msg:
        msg.body('https://54de497f262f.ngrok.io/api/movie/')
        responded = True
    if 'me' in incoming_msg:
        msg.body(incoming_num)
        responded = True
    if 'map' in incoming_msg:
        msg.body('Here is the Location you are Looking for:')
        msg.body('https://goo.gl/maps/PJ9YnE3kBvkjow8e8')
        responded = True
    if 'subscribe' in incoming_msg:
        print(info)
        r = requests.post('https://localhost:44325/api/movie/', json=info, verify=False)
        hello = r.text
        msg.body(hello)
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)
