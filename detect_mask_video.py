# import the necessary packages
import time
import cv2
import os
import serial

arduino = serial.Serial('COM3', 9600)
time.sleep(2)
print("Connection to arduino...")

def serial_commute(x_coord):
	data = "X{0:f}".format(x_coord)
	arduino.write(data.encode('utf-8'))
	# print("Coordinate is :", data)

while (True):
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()