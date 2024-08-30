import cv2
import numpy as np
import torch
import time

# Load the YOLOv5 model from PyTorch Hub (ensure you have the correct model file)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')
model.eval()

# Initialize webcam (0 is the default camera, change it if you have multiple cameras)
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from webcam")
            break

        # Convert frame from BGR to RGB as the model expects RGB format
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform object detection
        results = model(img_rgb)

        # Extract detection results
        detections = results.pandas().xyxy[0]  # pandas DataFrame format of detections

        # Print detection results
        for index, row in detections.iterrows():
            print(f"Detection {index}: Class: {row['name']}, Confidence: {row['confidence']:.2f}, "
                  f"Coordinates: ({row['xmin']:.0f}, {row['ymin']:.0f}) -> ({row['xmax']:.0f}, {row['ymax']:.0f})")
		
        print('-----------------')
		
        # Exit loop on 'ESC' key press
        if cv2.waitKey(1) & 0xFF == 27:
            break

        # Sleep to allow time for processing and reduce CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user, shutting down...")

finally:
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

