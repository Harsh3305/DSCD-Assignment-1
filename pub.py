# multipart_pub.py
import zmq
import time

from src.model.client import Client

host = "127.0.0.1"
port = "8081"

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.PUB)

# Binds the socket to a predefined port on localhost
socket.bind("tcp://{}:{}".format(host, port))

time.sleep(1)

# Sends a multipart message
socket.send_string("RESPONSE_JOIN_SERVER", flags=zmq.SNDMORE)
# Sends the second part

socket.send_json({
    "client_uuid": "15115",
    "client_address": "ioer iig ",
    "Author": "Harsh3305",
    "Type": "None",
    "Content": "DSCD sucks",
    "Date": "2023/01/20"
})

