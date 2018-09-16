#!/usr/bin/python3
import pytesseract
#from pytesseract import image_to_string
from PIL import Image
import argparse
import cv2
import os
import subprocess

#construct the arguments and prase it
ap = argparse.ArgumentParser()

#The path to the image we re sending through the OCR system. [i = argument/parameter | image = argument variable]
ap.add_argument("-i","--image", required=True, help="Path of the Captcha Image to Read")

#The preprocessing method. This switch is optional. This preprocessing can accept two values (Threshold or Blur)
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="Type of preprocessing is done | thresh OR blur")

#store arguments in args variable
args = vars(ap.parse_args())

#load the sample image and convert it into grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#check if user set preprocesing arguments
#image [generate binary image - image processing]
if args["preprocess"]=="thresh":
    gray = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#noise [if image got more noise ( Median blurring ). this line segment can use to remove it ]
if args["preprocess"]=="blur":
    gray = cv2.medianBlur(gray,3)

#write grascale image to current directory, so that we can use it with pytessract
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename,gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file

text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)

#print captured text
print(text)

#get output
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)





