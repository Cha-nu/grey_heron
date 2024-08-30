import cv2
import numpy as np
import torch
from picamera2 import Picamera2, Preview
from PIL import Image
import time

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')
model.eval()
	
picam = Picamera2()
#camera_config = picam.create_preview_configuration()
#picam.configure(camera_config)
#picam.start_preview(Preview.QT)
picam.start()

cv2.namedWindow('YOLOv5 OD', cv2.WINDOW_NORMAL)

try:
	while True:
	
		frame = picam.capture_array()
		
		img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		
		results = model(img_rgb)
		
		annotated_frame = np.squeeze(results.render())
		
		cv2.imshow('OD', annotated_frame)
		
		if cv2.waitKey(1) & 0xFF == 27:
			break
		time.sleep(1)


except KeyboardInterrupt:
	print("Truns_off")
	
finally:
	picam.stop()
	cv2.destroyAllWindows()	
