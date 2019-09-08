from __future__ import print_function
import requests
import json
import cv2
import time
import cv2
import numpy as np
import socket
import sys
import pickle
import struct

addr = 'http://35.245.236.232:5000'
test_url = addr + '/api/test'

def get_frames(video_name):	
	cap = cv2.VideoCapture(0)
	# warmup
	for i in range(5):
		cap.read()
	while True:
		ret, frame = cap.read()
		if ret:
			yield frame
		else:
			break


# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}
for frame in get_frames(""):
	start = time.time()
	#img = cv2.imread('/Users/pv/Desktop/pysot/tools/image.png')
	# encode image as jpeg
	_, img_encoded = cv2.imencode('.png', frame)

	#Serialize frame
	data = pickle.dumps(frame)

	# Send message length first
	message_size = struct.pack("L", len(data)) ### CHANGED

	# Then data
	#clientsocket.sendall(message_size + data)

	# send http request with image and receive response
	response = requests.post(test_url, data=data, headers=headers)
	# decode response
	print(response.text + " " + str(time.time()-start))
	#time.sleep(0.17)