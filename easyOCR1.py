import easyocr
import cv2
import matplotlib.pyplot as plt

# Load the image
image_path = 'bill.jpg'
image = cv2.imread(image_path)

# Convert image from BGR to RGB (for matplotlib display)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # You can add other languages, e.g. ['en', 'hi']

# Perform OCR on the image
results = reader.readtext(image_path)

# Print the text results
print("Detected Text:")
for (bbox, text, prob) in results:
    print(f"{text} (Confidence: {prob:.2f})")

# Optional: Display the image with bounding boxes
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

# Show the final image with OCR annotations
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("OCR Results")
plt.axis("off")
plt.show()
