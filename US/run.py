from flask import Flask, request
from socket import *
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, this is the US application!', 200

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return 'Something went wrong or missing parameters.', 400

    ip_request = {
        'TYPE': 'A',
        'NAME': hostname
    }
    server_name, server_port = as_ip, 53533
    message = json.dumps(ip_request)
    us_socket = socket(AF_INET, SOCK_DGRAM)
    us_socket.sendto(message.encode(), (server_name, server_port))
    recv, server_address = us_socket.recvfrom(2048)
    r = json.loads(recv.decode())
    ip_address = r['VALUE']
    us_socket.close()
    html = 'http://{}:{}/fibonacci?number={}'.format(ip_address, fs_port, number)
    link = urlopen(html)
    return link.read(), 200

app.run(host='0.0.0.0', port=8080, debug=True)
