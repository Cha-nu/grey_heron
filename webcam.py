import cv2
import numpy as np
import torch
import time

# Load the YOLOv5 model from PyTorch Hub (ensure you have the correct model file)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
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

        # Perform object detection
                results = model(frame)

        # Render the results on the frame
                annotated_frame = np.squeeze(results.render())
        
                end_time = time.time()
        
                print(end_time - start_time)

        # Display the resulting frame
                cv2.imshow('YOLOv5 OD', annotated_frame)
        
                for *box, conf, cls in results.xyxy[0]:
                        x1, y1, x2, y2 = [int(i) for i in box]
                        label = model.names[int(cls)]
                if label == 'balloons':
                        print("Suspected balloon object detected!")
                        cv2.imwrite('photo.jpg', frame)
                        break

        # Break loop on 'ESC' key press
                if cv2.waitKey(1) & 0xFF == 27:
                        break


except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")

finally:
        # Release resources and close windows
        cap.release()
        cv2.destroyAllWindows()
