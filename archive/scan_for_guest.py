import moondream as md
from PIL import Image
import time

# Load the ultra-lightweight 0.5B int8 model
# Download this specific file to your /work folder first
model = md.vl(model="./moondream-0_5b-int8.mf")

def scan_for_guest(image_path):
    image = Image.open(image_path)
    
    # Encode image (This takes ~8-9s on a Pi)
    start_time = time.time()
    encoded_image = model.encode_image(image)
    
    # Detect objects (Returns x_min, y_min, x_max, y_max)
    # We ask for 'person' to identify guests
    results = model.detect(encoded_image, "person")["objects"]
    
    print(f"Scan took {time.time() - start_time:.2f} seconds")
    
    if len(results) > 0:
        print(f"Guest detected! Found {len(results)} person(s).")
        # You can use the first result to guide movement
        # results[0] contains {'x_min': ..., 'y_min': ...}
        return True, results[0]
    
    return False, None

# Mock execution for your Docker environment
# replace 'test.jpg' with a real path when on the Pi
# found, coords = scan_for_guest("test.jpg")