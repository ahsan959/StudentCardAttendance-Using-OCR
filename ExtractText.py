import cv2
import pytesseract

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# Initialize camera object
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1024)

# Create a file to store the extracted text
output_file = open("output.csv", "w", encoding="utf-8")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Apply image processing techniques to enhance text extraction
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)

    # Use OCR to extract text from image
    text = pytesseract.image_to_string(gray)

    # Display text on screen
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Quit program when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("All Text Extracted ")
        # Save extracted text to file
        # output_file.write(text)
        print(text)
        break

# Release camera, close file, and close window
cap.release()

cv2.destroyAllWindows()

output_file.close()