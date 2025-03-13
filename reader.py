import easyocr   # For OCR text detection
import cv2       # For loading images
import numpy as np  # For handling bounding boxes as arrays

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Global dictionary to store detected text locations
detected_regions = {}

# Step 1: Extract text from the image
text = reader.readtext("player_profile1.png", detail=0)

governor_name = None
power = None
kill_points = None

# Extract only relevant data (values, not labels)
for i, word in enumerate(text):
    if word == "Governor" and i + 1 < len(text):
        governor_name = text[i + 1]  # The name appears right after "Governor"
    elif "Power" in word and i + 1 < len(text):
        power = text[i + 1]
    elif "Kill Points" in word and i + 1 < len(text):
        kill_points = text[i + 1]

def detect_text_regions(img_path):
    """Detects text locations of the values (Governor Name, Power, Kill Points)."""
    global detected_regions
    img = cv2.imread(img_path)  # Load the image

    # Run OCR to detect text and bounding boxes
    results = reader.readtext(img, detail=1)  # detail=1 returns coordinates

    # Store bounding boxes for values, not labels
    for bbox, text, conf in results:
        if text == governor_name:
            detected_regions["Governor"] = bbox
        elif text == power:
            detected_regions["Power"] = bbox
        elif text == kill_points:
            detected_regions["Kill Points"] = bbox

    detected_regions = {key: [[int(x), int(y)] for x, y in bbox] for key, bbox in detected_regions.items()}
    print("🔹 Cleaned Detected Regions:", detected_regions)


# Step 2: Detect regions for the extracted values
detect_text_regions("player_profile1.png")

# Print cleaned data
print("\nExtracted Data:")
print(f"Governor Name: {governor_name}")
print(f"Power: {power}")
print(f"Kill Points: {kill_points}")
