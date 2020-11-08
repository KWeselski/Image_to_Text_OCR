import flask
from flask import Flask, request, render_template, redirect, url_for, session ,send_from_directory
from PIL import Image
import cv2
import pytesseract
import imutils
import datetime
import numpy as np
import io
import os

app = Flask(__name__)
app.secret_key = '\xaai\xe42\xf7\xdfEN\x02\x17\x9e\x9b\xcd-\xcf\x0cL\xc4\xbb\xeb\xa4\x10\x06'
app_dir = os.path.dirname(os.path.abspath(__file__))

def get_grayscale(image):
    image_ = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)
    return Image.fromarray(image_)
# noise removal
def remove_noise(image):
    return cv2.medianBlur(np.array(image),5)
#thresholding
def thresholding(image):
    return cv2.threshold(np.array(image),205,255, cv2.THRESH_BINARY)[1]
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

@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

@app.route('/upload', methods=['POST'])
def upload():
    img_path = os.path.join(app_dir,'static/images/')
    if not os.path.isdir(img_path):
        os.mkdir(img_path)
    upload = request.files.getlist('file')[0]
    print('File name: {}'.format(upload.filename))
    file = upload.filename

    destination = "/".join([img_path,file])
    upload.save(destination)
    return render_template("processing.html",image_name=file)

@app.route('/grayscale', methods=['POST'])
def grayscale():
    filename = request.form['image']
    file_path = os.path.join(app_dir,'static/images/')
    destination = "/".join([file_path,filename])
    img = Image.open(destination)
    if img.mode == 'RGB':
        print('Wykonało')
        img = get_grayscale(img)
    destination = "/".join([file_path, 'temp.png'])
    #if os.path.isfile(destination):
    #    os.remove(destination)
    img.save(destination)
    #send_image(filename)
    send_image('temp.png')
    return render_template("processing.html",image_name='temp.png')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        image = request.files['file'].read()
        text = pytesseract.image_to_string(Image.open(io.BytesIO(image)))  
        image = Image.open(io.BytesIO(image)).convert('RGB')
        #image = cv2.resize(np.array(image), None, fx=0.5, fy=0.5)
        img_gray = get_grayscale(image)
        adaptive_threshold = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
        #img_gray = imutils.resize(img_gray, width=640) 
        img_thresh = thresholding(img_gray)
        img_dilate = dilate(img_thresh)
        img_erode = erode(img_thresh)
        #cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        custom_config = r'--psm 3'    
        text_gray = pytesseract.image_to_string(img_gray, config=custom_config)
        text_adaptive = pytesseract.image_to_string(adaptive_threshold, config=custom_config)
        text_thresh = pytesseract.image_to_string(img_thresh, config=custom_config)
        text_dilate = pytesseract.image_to_string(img_dilate,config=custom_config)
        text_erode = pytesseract.image_to_string(img_erode, config=custom_config)
        session['data'] = {
            'text': text,
            'text_adaptive': text_adaptive,
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
            text = data['text'],
            text_adaptive = data['text_adaptive'],
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