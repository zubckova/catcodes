from base64 import b64encode
import requests
from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True

def request(address):
    try:
        if requests.get(address).status_code == 200:
            return True
    except:
        return False

def detect_work_addresses(address):

    protocols = [
        "https:", "http:"
    ]

    addresses = []

    for protocol in protocols:
        if request(protocol+"//"+address): addresses.append(protocol+"//"+address)

    return addresses

def get_cat_by_status(status):
    response = requests.get(f'https://http.cat/{status}')
    return response.content

@app.route('/<address>')
def show_status(address):
    address = detect_work_addresses(address)
    try:
        response = requests.get(address[0])
        return render_template('/app.html', status=response.status_code)
    except:
        return "Address doesn't exist"
