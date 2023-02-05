import cv2
import os
from fpdf import FPDF
import depthai as dai
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from gtts import gTTS 
from playsound import playsound
import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)
print("Connection to arduino...")

def serial_commute(x_coord):
	data = "X{0:f}".format(x_coord)
	arduino.write(data.encode('utf-8'))
	# print("Coordinate is :", data)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    # os.system("mpg321 speech.mp3")

# Define the window name and size
window_name = "Capturing Images"
window_size = (1080, 1920)

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
xoutPreview = pipeline.create(dai.node.XLinkOut)

xoutPreview.setStreamName("preview")

# Properties
camRgb.setPreviewSize(*window_size)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setInterleaved(True)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Create the OpenCV window
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, *window_size)

# Define the directory to save the images
save_dir = "images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Initialize the image index
img_index = 0

cap = cv2.VideoCapture(0)

# Linking
camRgb.preview.link(xoutPreview.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    preview = device.getOutputQueue('preview')

    while True:
        previewFrame = preview.get()

        # Show 'preview' frame as is (already in correct format, no copy is made)
        cv2.imshow("preview", previewFrame.getFrame())

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Save the image as a PNG file
            img_path = os.path.join(save_dir, f"img_{img_index}.png")
            rotated_image = cv2.rotate(previewFrame.getFrame(), cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Split the image in half vertically
            frame_height, frame_width, _ = rotated_image.shape
            left_half = rotated_image[:, :frame_width//2]
            right_half = rotated_image[:, frame_width//2:]

            cv2.imwrite(img_path, left_half)
            img_index += 1
            
            img_path = os.path.join(save_dir, f"img_{img_index}.png")
            cv2.imwrite(img_path, right_half)
            img_index += 1

            # Turn the page via arduino
            serial_commute(1)
            time.sleep(5)
        elif key == ord('q'):
            break

# Destroy the OpenCV window
cv2.destroyAllWindows()

# Combine the images into a single PDF file
pdf_path = "book.pdf"
pdf = FPDF()
for i in range(img_index):
    img_path = os.path.join(save_dir, f"img_{i}.png")
    cover = Image.open(img_path)
    width, height = cover.size

    # convert pixel in mm with 1px=0.264583 mm
    width, height = float(width * 0.264583), float(height * 0.264583)

    # given we are working with A4 format size 
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    # get page orientation from image size 
    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    pdf.add_page(orientation=orientation)

    pdf.image(img_path, 0, 0, width, height)
pdf.output(pdf_path, "F")

# Convert the PDF pages to images
images = convert_from_path(pdf_path)

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Iterate through the pages of the PDF
for i, image in enumerate(images):
    # OCR the image
    text = pytesseract.image_to_string(image)
    
    # Print the text
    print(f"Page {i + 1}:")
    print(text)

text_to_speech(text)