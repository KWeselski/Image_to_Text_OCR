import flask
from flask import Flask, request, render_template, redirect, url_for, session
from PIL import Image
import cv2
import pytesseract
import imutils
import datetime
import numpy as np
import io


app = Flask(__name__)
app.secret_key = '\xaai\xe42\xf7\xdfEN\x02\x17\x9e\x9b\xcd-\xcf\x0cL\xc4\xbb\xeb\xa4\x10\x06'


def get_grayscale(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)
# noise removal
def remove_noise(image):
    return cv2.medianBlur(np.array(image),5)
#thresholding
def thresholding(image):
    return cv2.threshold(np.array(image),215,255, cv2.THRESH_BINARY)[1]
#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(np.array(image), kernel, iterations = 1)  
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(np.array(image), kernel, iterations = 1)

@app.route('/')
def index():
    return render_template("index.html", title="Image Converter")

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        image = request.files['file'].read()
        image = Image.open(io.BytesIO(image)).convert('RGB')
        img_gray = get_grayscale(image)
        #img_gray = imutils.resize(img_gray, width=640) 
        img_thresh = thresholding(img_gray)
        img_dilate = dilate(img_thresh)
        img_erode = erode(img_thresh)
        #cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
         
        custom_config = r'--oem 3 --psm 6'    
        text_gray = pytesseract.image_to_string(img_gray, timeout =5, config=custom_config)
        text_thresh = pytesseract.image_to_string(img_thresh,timeout =5 ,config=custom_config)
        text_dilate = pytesseract.image_to_string(img_dilate,timeout =5 ,config=custom_config)
        text_erode = pytesseract.image_to_string(img_erode,timeout =5 ,config=custom_config)
        session['data'] = {
            'text_gray': text_gray,
            'text_thresh':text_thresh,
            'text_dilate':text_dilate,
            'text_erode':text_erode
        }
        return redirect(url_for('result'))

@app.route('/result')
def result():
    if "data" in session:
        data = session['data']
        print(data)
        return render_template(
            'text.html',
            title= "Text scanned",
            text_gray= data['text_gray'],
            text_thresh=data['text_thresh'],
            text_dilate=data['text_dilate'],
            text_erode=data['text_erode'],
        )
    else:
        return "Error"

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    app.run(debug=True)