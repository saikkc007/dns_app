from flask import Flask, request
from socket import *
import json

app = Flask(__name__)

server_port = 53533
as_socket = socket(AF_INET, SOCK_DGRAM)
as_socket.bind(('', server_port))

while True:
    message, client_address = as_socket.recvfrom(2048)
    recv = json.loads(message.decode())

    if len(recv) == 4:  # Registration
        with open('./database.txt', 'a') as outfile:
            json.dump(recv, outfile)
            message = '201'
    elif len(recv) == 2:  # DNS Query
        with open("./database.txt", 'r', encoding='utf-8') as outfile:
            for line in outfile.readlines():
                data = json.loads(line)
                if recv['TYPE'] == data['TYPE'] and recv['NAME'] == data['NAME']:
                    message = json.dumps(data)
                else:
                    message = 'Something went wrong or fs not registered.'
    else:
        message = 'ERROR'

    as_socket.sendto(message.encode(), client_address)
