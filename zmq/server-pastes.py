import zmq
import random
import sys
import time
import redis
import base64

port = "5556"
pystemonpath = "<home directory where the pasties live>"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

r = redis.StrictRedis(host='localhost', db=10)
# 101 pastes processed feed
# 102 raw pastes feed

while True:
    time.sleep(.1)
    topic = 101
    paste = r.lpop("pastes")
    if paste is None:
        continue
    socket.send("%d %s" % (topic, paste))
    topic = 102
    messagedata = open(pystemonpath+paste).read()
    socket.send("%d %s %s" % (topic, paste, base64.b64encode(messagedata)))
