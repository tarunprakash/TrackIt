import flask
from flask import Flask

app = Flask(__name__)

tracking_threshold = 0.3

@app.route("/")
def index():
	with open("instructions.txt") as file:
		f = file.readline().strip().split()

		if not f:
			print("EMPTY FILE")
			return "STILL STILL False"
		if len(f) < 3:
			f.append("0.0")
		print(f)
		confidence = float(f[-1])
		ins = f[:-1]
		good_track = False

		if confidence > tracking_threshold:
			good_track = True

		ret = " ".join(ins) + " " + str(good_track)

		return ret

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
