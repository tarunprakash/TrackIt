from flask import Flask, request
import pickle, struct
import numpy as np
import jsonpickle
import cv2


app = Flask(__name__)
@app.route('/api/test', methods = ['POST'])
def test():
		r = request
		nparr = np.fromstring(r.data, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		while len(data) < payload_size:
			data += conn.recv(4096)

		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED
		
		frame_data = data[:msg_size]
		data = data[msg_size:]

		# Extract frame
		frame = pickle.loads(frame_data)

		response = {'message' : 'image received.{}'.format(len(frame))}
		response_pickled = jsonpickle.encode(response)
		return Response(response = response_pickled, status = 200, mimetype = "application/json")

@app.route("/")
def index():
	return "Webserver Running!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)