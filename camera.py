# Import opencv for computer vision stuff
import cv2
import pytesseract

# Import matplotlib so we can visualize an image
from matplotlib import pyplot as plt

# Connect to capture device
cap = cv2.VideoCapture(0)

ret, frame = cap.read()

img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb))

plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.show()

# # Video Capture
# # Loop through every frame until we close our webcam
# while cap.isOpened(): 
#     ret, frame = cap.read()

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Apply OCR using pytesseract library
#     text = pytesseract.image_to_string(gray)

#     # Print the extracted text
#     print(text)
#     # Show image 
#     cv2.imshow('Webcam', frame)
    
#     # Checks whether q has been hit and stops the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         break