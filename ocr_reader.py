import easyocr   # OCR text detection
import cv2       # Image processing
import numpy as np
from PIL import Image  # Cropping images for speed

# Global EasyOCR reader
reader = easyocr.Reader(['en'])

from PIL import Image

def get_region(img_path, ocr_results, anchor_text, offset):
    """
    img_path: path to image
    ocr_results: OCR list from reader.readtext()
    anchor_text: the string to search for (e.g. 'Kill Statistics')
    offset: number of items after the anchor to get (e.g. 2)
    """
    img = Image.open(img_path)

    # Find the index of the anchor string
    anchor_index = next(i for i, (_, text, _) in enumerate(ocr_results) if anchor_text.lower() in text.lower())
    
    # Calculate target index
    target_index = anchor_index + offset
    if not (0 <= target_index < len(ocr_results)):
        raise IndexError("Offset leads to invalid index.")

    # Get bounding box of the target
    box = ocr_results[target_index][0]
    points = [[int(x), int(y)] for x, y in box]
    x1 = min(p[0] for p in points)
    y1 = min(p[1] for p in points)
    x2 = max(p[0] for p in points)
    y2 = max(p[1] for p in points)

    cropped = img.crop((x1, y1, x2, y2)).convert("RGB")
    cropped.save(f"debug_region_from_{anchor_text.replace(' ', '_')}_{offset}.png")

    return box


def get_text(img_path, box):
    img = Image.open(img_path)

    x_coords = [p[0] for p in box]
    y_coords = [p[1] for p in box]
    x1, x2 = min(x_coords), max(x_coords)
    y1, y2 = min(y_coords), max(y_coords)

    cropped = img.crop((x1, y1, x2, y2))
    result = reader.readtext(np.array(cropped), detail=0)

    return result[0] if result else "N/A"