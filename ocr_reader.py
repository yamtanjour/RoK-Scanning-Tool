import easyocr   # OCR text detection
import cv2       # Image processing
import numpy as np
from PIL import Image  # Cropping images for speed

# Global EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_value_regions(img_path):
    
    img = cv2.imread(img_path)
    # Use detail=1 to get bounding boxes, text, and confidence values.
    results = reader.readtext(img, detail=1)
    print("OCR Results:", results)
    
    detected_regions = {}
    
    # Loop through the results (make sure there's at least one following result)
    for i in range(len(results) - 1):
        # Skip if current result does not have enough items.
        if len(results[i]) < 3 or len(results[i + 1]) < 1:
            continue

        # Use only the first three items (bbox, text, confidence)
        bbox, detected_text, _ = results[i][:3]
        lower_text = detected_text.lower()

        # Based on the label found, assign a region from one of the following OCR results.
        # Adjust the index offsets as necessary for your layout.
        if "civilization" in lower_text and "profile" not in lower_text:
            detected_regions["Governor"] = results[i + 1][0]
        if "power" in lower_text:
            # For example, use the next next result for power.
            detected_regions["Power"] = results[i + 3][0]
        if "kill points" in lower_text:
            # And maybe two results ahead for kill points.
            detected_regions["Kill Points"] = results[i + 3][0]
    
    # For debugging: open the image with PIL and save cropped regions.
    debug_img = Image.open(img_path)
    for key, box in detected_regions.items():
        # Convert each coordinate to integer values.
        box_int = [[int(x), int(y)] for x, y in box]
        # Use the top-left and bottom-right points for cropping.
        x1, y1 = box_int[0]
        x2, y2 = box_int[2]
        cropped = debug_img.crop((x1, y1, x2, y2))
        debug_filename = f"debug_{key}.png"
        cropped.save(debug_filename)
        print(f"Saved debug screenshot for {key} as: {debug_filename}")
        
        print(detected_regions)
    
    print(detected_regions)
    return detected_regions


def extract_values(img_path, regions):

    # Helper function to do the actual cropping and OCR
    def extract_text_from_box(pil_image, box):
        # box is a list of four points: top-left, top-right, bottom-right, bottom-left
        x1, y1 = box[0]
        x2, y2 = box[2]  # bottom-right corner
        x1 -= 30
        x2 += 100
        cropped_img = pil_image.crop((x1, y1, x2, y2))
        # OCR on the cropped region
        result = reader.readtext(np.array(cropped_img), detail=0)
        return result[0] if result else "N/A"

    # Initialize return values
    governor_name = "N/A"
    power_val = "N/A"
    kill_points_val = "N/A"

    # Open the original image once
    pil_img = Image.open(img_path)

    # Extract each value if we have its bounding box
    if "Governor" in regions:
        governor_name = extract_text_from_box(pil_img, regions["Governor"])
    if "Power" in regions:
        power_val = extract_text_from_box(pil_img, regions["Power"])
    if "Kill Points" in regions:
        kill_points_val = extract_text_from_box(pil_img, regions["Kill Points"])

    return governor_name, power_val, kill_points_val

