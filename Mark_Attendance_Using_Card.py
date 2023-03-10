import cv2
import pytesseract
import re
import csv

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(2,1024)

# Create a CSV file to store the extracted text
with open('extracted_text.csv', mode='w', newline='',encoding="utf-8") as file:
    writer = csv.writer(file)

    # Start capturing frames from the camera
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use OCR to extract text from the image
        text = pytesseract.image_to_string(gray)

        # Clean the text by removing special characters and extra whitespace
        text = re.sub(r'[^\w\s]', '', text).strip()

        # Split the text into words
        words = text.split()

        # Remove empty values and duplicate words
        words = set(filter(None, words))

        # Check if each word is already present in the file, and save only new words
        with open('extracted_text.csv', mode='r') as f:
            reader = csv.reader(f)
            existing_words = set(row[0] for row in reader)
            new_words = words - existing_words

        # Write the new words to the file
        for word in new_words:
            if word:
                writer.writerow([word])

        # Display the original image with text overlay
        cv2.imshow('Extracted Text', frame)

        # Quit program if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera and close the CSV file
cap.release()
cv2.destroyAllWindows()
