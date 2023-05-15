from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np

import imutils
import time
import cv2
import os
import streamlit as st

def detect_and_predict_mask(frame, faceNet, maskNet,cnf=.5):
	
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
	faceNet.setInput(blob)
	detections = faceNet.forward()
	faces = []
	locs = []
	preds = []
    
	for i in range(0, detections.shape[2]):
		
		confidence = detections[0, 0, i, 2]
		if confidence > cnf:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)
			faces.append(face)
			locs.append((startX, startY, endX, endY))
    
	if len(faces) > 0:
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)
	
	return (locs, preds)


def video(face ='face_detector',model = 'mask_detector.model',cnf=.5):
	print("[INFO] loading face detector model...")
	prototxtPath = os.path.sep.join([face, "deploy.prototxt"])
	weightsPath = os.path.sep.join([face,"res10_300x300_ssd_iter_140000.caffemodel"])
	faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
	print("[INFO] loading face mask detector model...")
	maskNet = load_model(model)
	print("[INFO] starting video stream...")
	vs = VideoStream(src=cnf['input']).start()
	#vs = cv2.VideoCapture(0)
	time.sleep(2.0)
	
	while True:
		frame = vs.read()
		print(frame)
		frame = imutils.resize(frame, width=400)
		(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
		for (box, pred) in zip(locs, preds):
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred
			label = "Mask" if mask > withoutMask else "No Mask"
			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
			cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		cv2.imshow("Face Mask Detector", frame)
		key = cv2.waitKey(1)
		if key == ord('q') or cv2.getWindowProperty("Face Mask Detector", cv2.WND_PROP_VISIBLE) < 1:
			break
	
	cv2.destroyAllWindows()
	vs.stop()
if __name__  =='__main__':
	video()
