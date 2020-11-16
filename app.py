import flask
from flask import Flask, request, render_template, redirect, url_for, session ,send_from_directory
from PIL import Image
import cv2
import pytesseract
import datetime
import numpy as np
import io
import os
import base64

app = Flask(__name__)
app.secret_key = '\xaai\xe42\xf7\xdfEN\x02\x17\x9e\x9b\xcd-\xcf\x0cL\xc4\xbb\xeb\xa4\x10\x06'
app_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template("index.html", title="Image Converter")

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        image = request.form['imageInput']
        img = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
        text = pytesseract.image_to_string(img)
        print(text) 

        session['data'] = {
            'text': text,
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