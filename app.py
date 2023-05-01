#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import json, jsonify
import urllib.request
import os
from werkzeug.utils import secure_filename

import cv2 as cv
import numpy as np
import pytesseract
import sys
 
app = Flask(__name__,template_folder='template')
 
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
 
@app.route('/', methods=['POST'])
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
            imag = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("imag : ",imag)
            img = cv.imread(imag)
            text = pytesseract.image_to_string(img)
            print("###",type(text))

            output = text.strip()
            output = output.replace("\n'","")
            output = ''.join(output.splitlines())
            
            result ={
            "text" : output
            }
            # res.append(result)
        except Exception as e:
            print("Img is not found",e)
            pass
        return jsonify(result)
        # return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True)
