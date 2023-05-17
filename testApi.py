from flask import Flask, request, jsonify, json
import os
import urllib.request

from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

import cv2 as cv
import requests
import pytesseract
import sys 
app = Flask(__name__)
 
app.secret_key = "thakur_programmer__77"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    # return render_template('index.html')
    return '<h2 style=text-align:center; > Hola!! welcome to my Homepage!!</h2>'
 
@app.route('/get-text', methods=['POST'])
def upload_file():
    
    my_files = request.files
    imd = ImmutableMultiDict(my_files)
    imd1 = imd.to_dict(flat=False)
    file_key = ''
    for key in imd1:
        file_key = key
    files = request.files.getlist(file_key)
 
    print(files)
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True

            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("image_path : ",image_path)
                image = cv.imread(image_path)
                text = pytesseract.image_to_string(image)


                output = text.strip()
                output = output.replace("\n'","")
                final_text = ''.join(output.splitlines())
                
                result ={
                "text" : final_text
                }

            except Exception as e:
                print("Img is not found",e)
                print(f"error pytesserct not installed ! Install this package to resolve above error 'pip3 install pytesseract'")
                pass

        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify(result)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
""" Test the api is this working or not."""
@app.route('/api_testing')
def api_test():
    url = "http://167.71.4.12:5000/get-text"
    payload={}
    files=[
      ('file',('download.png',open('/home/dev09/Downloads/post.png','rb'),'image/png'))
    ]
    response = requests.request("POST", url, data=payload, files=files)
    print('response = ', response.text)
    json_obj = json.loads(response.text)
    return jsonify(
        message = str(json_obj['text']),
        is_error = False,
        status = 200,
    )

if __name__ == '__main__':
    app.run(debug=True)