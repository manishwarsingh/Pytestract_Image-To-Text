
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import json, jsonify
import urllib.request
import os
from werkzeug.utils import secure_filename

import cv2 as cv
import numpy as np
import pytesseract
import sys
 
app = Flask(__name__,template_folder='templates')
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
    # return '<h2 style=text-align:center; > Hola! EveryOne welcome to my Homepage!!</h2>'
 
@app.route('/get-text', methods=['POST'])
def upload_image():
    # result ={}
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        # print('upload_image fileurl: ' + fileurl)

        try:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("image_path : ",image_path)
            image = cv.imread(image_path)
            text = pytesseract.image_to_string(image)
            print(type(text))

            output = text.strip()
            output = output.replace("\n'","")
            output_text = ''.join(output.splitlines())
            
            result ={
            "image_text" : output_text
            }
        except Exception as e:
            print("Img is not found", e)
            print(f"error pytesserct not installed ! Install this package to resolve above error 'pip3 install pytesseract'")
            pass
        return jsonify(result)
        # return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True )
