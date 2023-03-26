import requests
from db import Address, Code
from flask import Flask, render_template

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

def save_info_about_request(status, address):

    try:
        Code.create(
            url=Address.get(Address.url == address),
            status=status
        )
    except:
        url = Address.create(url=address)
        code = Code.create(url=url, status=status)
    

app = Flask(__name__)

@app.route('/<address>')
def show_status(address):
    address = detect_work_addresses(address)
    try:
        response = requests.get(address[0])
        status = response.status_code
        save_info_about_request(status, address[0])
        return render_template('/app.html', status=status)
    except NameError:
        return f"Address doesn't exist{NameError.name}"
