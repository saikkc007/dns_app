from flask import Flask, request
from socket import *
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, this is the FS application!', 200

def fibonacci(n):
    if n < 0:
        return "Input less than 0"
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci_number():
    try:
        num = int(request.args.get('number'))
        return 'Sequence: {0} ---> Fibonacci: {1}'.format(num, fibonacci(num)), 200
    except:
        return 'Something went wrong or input is not a number or less than 0.', 400

@app.route('/register', methods=['PUT'])
def register():
    req_data = request.get_json()
    hostname, ip, as_ip, as_port = req_data['hostname'], req_data['ip'], req_data['as_ip'], req_data['as_port']

    server_name, server_port = as_ip, 53533
    fs_socket = socket(AF_INET, SOCK_DGRAM) 
    dns_request = {
        'TYPE': 'A',
        'NAME': hostname,
        'VALUE': ip,
        'TTL': 10
    }
    message = json.dumps(dns_request)
    fs_socket.sendto(message.encode(), (server_name, server_port))

    message, server_address = fs_socket.recvfrom(2048)
    fs_socket.close()
    r = message.decode()
    if r == "201":
        return "Registration successful", 201
    else:
        return r, 400

app.run(host='0.0.0.0', port=9090, debug=True)
