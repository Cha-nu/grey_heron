import cv2
import numpy as np
import torch
import time

# Load the YOLOv5 model from PyTorch Hub (ensure you have the correct model file)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')
model.eval()

# Initialize webcam (0 is the default camera, change it if you have multiple cameras)
cap = cv2.VideoCapture(0)

# Create an OpenCV window to display the output
cv2.namedWindow('YOLOv5 OD', cv2.WINDOW_NORMAL)

try:
    while True:
        start_time = time.time()
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from webcam")
            break

        # Convert frame from BGR to RGB as the model expects RGB format
        #img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform object detection
        #results = model(img_rgb)
        results = model(frame)

        # Render the results on the frame
        annotated_frame = np.squeeze(results.render())
        
        end_time = time.time()
        
        print(end_time - start_time)

        # Display the resulting frame
        cv2.imshow('YOLOv5 OD', annotated_frame)

        # Break loop on 'ESC' key press
        if cv2.waitKey(1) & 0xFF == 27:
            break

        # Sleep to allow time for display and reduce CPU usage
        #time.sleep()

except KeyboardInterrupt:
    print("Interrupted by user, shutting down...")

finally:
    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()
