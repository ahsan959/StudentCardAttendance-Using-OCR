

import cv2
import pytesseract
import csv

# Set up video capture
cap = cv2.VideoCapture(0)

cap.set(3,1920)
cap.set(2,1024)

# # Set up pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

pytesseract.pytesseract.language = 'eng'

# Open the CSV file for writing and create a CSV writer object
with open('extracted_text.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Flag to keep track of whether the camera is on or off
    camera_on = True

    while True:
        # Read frame from camera
        ret, frame = cap.read()

        if ret:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Perform thresholding
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Perform text extraction using pytesseract
            text = pytesseract.image_to_string(thresh)

            # Remove empty values, commas, and spaces
            text = ' '.join(filter(lambda x: x.strip(), text.split('\n'))).replace(',', '')

            # Write the extracted text to the CSV file if it's not empty
            if text:
                writer.writerow([text])

            # Display the resulting frame
            cv2.imshow('frame', thresh)


        else:
            # If camera is turned off, set the flag to False and break out of the loop
            camera_on = False
            break

        # Quit program if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save the CSV file if there is any extracted text
    if camera_on:
        print('Extracted text saved to extracted_text.csv')

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()