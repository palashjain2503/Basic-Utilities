import easyocr
from pdf2image import convert_from_path
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Path to the PDF
pdf_path = 'acc.pdf'

# Convert PDF pages to images
images = convert_from_path(pdf_path, dpi=300)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Process each page
for page_num, pil_image in enumerate(images):
    print(f"\n--- OCR for Page {page_num + 1} ---")
    
    # Convert PIL image to OpenCV format
    open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    # Save temp image (optional, but good for debugging)
    image_path = f'page_{page_num + 1}.jpg'
    cv2.imwrite(image_path, open_cv_image)

    # OCR
    results = reader.readtext(open_cv_image)

    # Print text
    for (bbox, text, prob) in results:
        print(f"{text} (Confidence: {prob:.2f})")

    # Display result with bounding boxes
    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        
        cv2.rectangle(open_cv_image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(open_cv_image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show the annotated image
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
    plt.title(f"OCR Results - Page {page_num + 1}")
    plt.axis("off")
    plt.show()
