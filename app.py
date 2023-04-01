import base64
import requests
from db import Address, Code
from flask import Flask, render_template
from PIL import Image
from io import BytesIO
from io import StringIO
from pymemcache.client import base

client = base.Client(('localhost', 11211))

def request(address):
    try:
        if requests.get(address).status_code == 200:
            return True
    except:
        return False

def detect_work_addresses(address):

    print(address)

    protocols = [
        "https:", "http:"
    ]

    addresses = []

    if "https://" in address or "http://" in address: 
        addresses.append(address)
    else:
        for protocol in protocols:
            test_address = protocol+"//"+address
            if request(test_address): 
                addresses.append(test_address)
    print(addresses)
    return addresses

def get_cat_by_status(status):
    response = requests.get(f'https://http.cat/{status}')
    return response.content

def get_image_by_status(status, format="string"):
    response = requests.get(f'https://http.cat/{status}')
    img = Image.open(BytesIO(response.content))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return base64_data

def check_memory(status):
    if client.get(f'{status}'):
        print("Image from cache.")
        return str(client.get(f'{status}'), 'utf-8')
    else: 
        image_binary = get_image_by_status(status)
        client.set(f'{status}', image_binary)
        print("Image is downloaded.")
        return str(image_binary, 'utf-8')
    

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

@app.route('/<path:address>')
def show_status(address):
    address = detect_work_addresses(address)

    try:
        response = requests.get(address[0])
        status = response.status_code
        image = check_memory(status)
        save_info_about_request(status, address[0])
        return render_template('/app.html', status=status, image=image)
    except NameError:
        return f"Address doesn't exist{NameError.name}"
