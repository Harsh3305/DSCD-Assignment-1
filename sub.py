# multipart_sub.py
import zmq

host = "127.0.0.1"
port = "8080"

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Connects to a bound socket
socket.connect("tcp://{}:{}".format(host, port))

# Subscribes to all topics
socket.subscribe("ML")
# Receives a multipart message
topic = socket.recv_string()
print(topic)
client = socket.recv_json()
print(client)
