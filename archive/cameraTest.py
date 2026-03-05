import cv2

# Try indices 0, 1, and 2 if 0 doesn't work
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam. Check if another app is using it or permissions.")
else:
    ret, frame = cap.read()
    if ret:
        print(f"Success! Frame captured with shape: {frame.shape}")
    else:
        print("Webcam found, but could not read a frame.")

cap.release()