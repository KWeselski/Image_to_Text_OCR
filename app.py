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
@app.route('/')
def index():
    return render_template("index.html", title="Image Converter")

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        session_time = datetime.datetime.now()
        image = request.files['file'].read()
        image = Image.open(io.BytesIO(image)).convert('RGB')
        img_gray = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2GRAY)
        img_gray = imutils.resize(img_gray, 1200, 1880)      
        text = pytesseract.image_to_string(img_gray)
        session['data'] = {
            'session_time': str((datetime.datetime.now()- session_time).total_seconds()),
            'text': text
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
        )
    else:
        return "Error"

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    app.run(debug=True)