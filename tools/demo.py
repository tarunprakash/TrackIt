from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import argparse

import cv2
import torch
import numpy as np
from glob import glob


from pysot.core.config import cfg
from pysot.models.model_builder import ModelBuilder
from pysot.tracker.tracker_builder import build_tracker

torch.set_num_threads(1)

config = "experiments/siamrpn_alex_dwxcorr/config.yaml"
snapshot = "experiments/siamrpn_alex_dwxcorr/model.pth"
vidName = ''
instruction = ["STILL", "STILL"]


## minimum confidence
tracking_threshold = 0.3

thresh_box_dimensions = (200,150)


def get_frames(video_name):	
	cap = cv2.VideoCapture(1)
	# warmup
	for i in range(5):
		cap.read()
	while True:
		ret, frame = cap.read()
		if ret:
			yield frame
		else:
			break



def main():
	# load config
	cfg.merge_from_file(config)
	cfg.CUDA = torch.cuda.is_available()
	device = torch.device('cuda' if cfg.CUDA else 'cpu')

	# create model
	model = ModelBuilder()

	# load model
	model.load_state_dict(torch.load(snapshot,
		map_location=lambda storage, loc: storage.cpu()))
	model.eval().to(device)

	# build tracker
	tracker = build_tracker(model)

	first_frame = True

	video_name = 'webcam'
	cv2.namedWindow(video_name, cv2.WND_PROP_FULLSCREEN)

	for frame in get_frames(vidName):
		frame = cv2.flip( frame, 1 )
		instruction = ["STILL", "STILL"]
		font_color = (0,255,0)
		frameDim = frame.shape
		window_center = (int(frameDim[1]/2), int(frameDim[0]/2))
		if first_frame:
			try:
				init_rect = cv2.selectROI(video_name, frame, False, False) ## rectangle is in format (topX,topY,width,height)
				##print(init_rect)
			except:
				exit()
			tracker.init(frame, init_rect)
			first_frame = False
		else:
			outputs = tracker.track(frame)
			confidence = outputs['best_score']
			
			if confidence < tracking_threshold:
				font_color = (0,0,255)

			bbox = list(map(int, outputs['bbox']))
			boxCenter = (int((bbox[0]+(bbox[0]+bbox[2]))/2), int((bbox[1]+(bbox[1]+bbox[3]))/2))

			##print(boxCenter, window_center)

			cv2.circle(frame, boxCenter, 5, (0,255,0), -1) ## center of bounding box
			##print(window_center, winDim)
			cv2.circle(frame,window_center, 5, (255,0,0), -1) ## center of window

			cv2.rectangle(frame, (bbox[0], bbox[1]), ## draw bounding box
						  (bbox[0]+bbox[2], bbox[1]+bbox[3]),
						  font_color, 3)
			cv2.rectangle(frame, (window_center[0]-thresh_box_dimensions[0], window_center[1]-thresh_box_dimensions[1]),
							(window_center[0]+thresh_box_dimensions[0], window_center[1]+thresh_box_dimensions[1]),
							(255,0,0), 3) ## draw window center

			## draw confidence text
			cv2.putText(frame,str(confidence), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2)

			## check x pos
			if boxCenter[0] > window_center[0]+thresh_box_dimensions[0]:
				instruction[0] = "RIGHT"
			elif boxCenter[0] < window_center[0] - thresh_box_dimensions[0]:
				instruction[0] = "LEFT"

			## check y pos
			if boxCenter[1] > window_center[1]+thresh_box_dimensions[1]:
				instruction[1] = "DOWN"
			elif boxCenter[1] < window_center[1]-thresh_box_dimensions[1]:
				instruction[1] = "UP"

			## draw confidence text
			cv2.putText(frame," ".join(instruction), (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2)

			with open("instructions.txt", "w") as file:
				print(" ".join(instruction) + " " + str(confidence))
				file.write(" ".join(instruction) + " " + str(confidence))
			#yield " ".join(instruction)

			cv2.imshow(video_name, frame)
			k = cv2.waitKey(33)
			if k==27: ## escape key to stop
				with open("instructions.txt", "w") as file:
					file.write("STILL STILL 0.0")
				break
			elif k==32: ## space bar to change selection
				first_frame = True


if __name__ == '__main__':
	main()
