import cv2
import torch
import numpy as np

#  Load YOLOv5 Model (using PyTorch Hub)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 2. Initialize Camera (External webcam is usually index 1)
cap = cv2.VideoCapture(1) 

def process_vslam(frame):
    """
    Placeholder for VSLAM logic (e.g., using pySLAM or simple ORB features)
    In a real app, you'd pass the frame to a SLAM object here.
    """
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(frame, None)
    return kp

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # --- YOLOv5 Inference ---
    results = model(frame)
    # Get detections: [xmin, ymin, xmax, ymax, confidence, class]
    detections = results.xyxy[0].cpu().numpy()

    # --- VSLAM Processing ---
    # Optional: Mask out 'person' or 'car' classes so SLAM ignores them
    mask = np.ones(frame.shape[:2], dtype="uint8") * 255
    for det in detections:
        if det[4] > 0.5:  # Confidence threshold
            cv2.rectangle(frame, (int(det[0]), int(det[1])), 
                          (int(det[2]), int(det[3])), (0, 255, 0), 2)
            # Example: Mask dynamic objects (e.g., class 0 is 'person')
            if int(det[5]) == 0: 
                mask[int(det[1]):int(det[3]), int(det[0]):int(det[2])] = 0

    # Execute SLAM only on static parts of the image
    keypoints = process_vslam(frame)
    frame = cv2.drawKeypoints(frame, keypoints, None, color=(0, 0, 255))

    cv2.imshow('VSLAM + YOLOv5', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()