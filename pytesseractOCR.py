import cv2
import pytesseract
import pandas as pd

# OPTIONAL: Tell pytesseract where tesseract.exe is (only if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
image = cv2.imread("bill.jpg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Run OCR with word-level data
df = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)

# Filter out low-confidence words
df = df[df.conf > 40]

# Group words into rows by line number
lines = df.groupby("line_num")["text"].apply(lambda x: " ".join(x)).tolist()

# Print each detected line
for line in lines:
    print(line)

# Optional: Save to CSV
pd.DataFrame(lines, columns=["Row"]).to_csv("bill_text_output.csv", index=False)
print("✅ OCR results saved to bill_text_output.csv")
