import cv2
import os

# Listen on any incoming data on port 1234
url = "udp://0.0.0.0:1234"

# These settings help OpenCV's FFMPEG backend sync up with the stream immediately
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "probesize;32|analyzeduration;0|flags;low_delay"

print("Waiting for video headers...")
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# Attempt to capture
for i in range(60):
    ret, frame = cap.read()
    if ret:
        print("--- SUCCESS! CAPTURED FRAME ---")
        print(f"Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cv2.imwrite("/work/proof_of_life.jpg", frame)
        break
    
if not ret:
    print("--- FAILURE: Still no frames. ---")

cap.release()