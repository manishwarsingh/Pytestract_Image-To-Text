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
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    # return render_template('index.html')
    return '<h2 style=text-align:center; > Hello!! welcome to my Homepage!!</h2>'
 
@app.route('/get-text', methods=['POST'])
def upload_file():
    
    # check if the post request has the file part
    # if 'file' not in request.files:
    #     resp = jsonify({'message' : 'No file part in the request'})
    #     resp.status_code = 400
    #     return resp
    # files = request.files.getlist('file')
    ''' Both logics are but the diffreence is above logic contains the files must during 
     test the api into the postman!! { " the below logic doesn;t need to pass the files name into the postman during the api "} '''
    
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

            # return jsonify(result)
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


if __name__ == '__main__':
    app.run(debug=True)