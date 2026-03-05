import cv2
import torch

# 1. Load YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 2. Connect to the Mac stream
# We use 'host.docker.internal' to reach the Mac host from inside Docker
stream_url = "udp://host.docker.internal:5000"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open UDP stream. Is ffmpeg running on the Mac?")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # YOLO Inference
    results = model(frame)
    
    # Render and Display
    results.render()
    cv2.imshow('VSLAM + YOLO Feed', results.ims[0])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()